import datetime

import pandas as pd
from io import BytesIO as IO
from functools import reduce
from operator import itemgetter
from datetime import datetime, date

from django.apps import apps
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import make_aware
from pandas._libs.tslibs.timestamps import Timestamp

from data_manager.constants import FEATURE_TYPES, FREQUENCY_USAGE_PREFERENCES, FREQUENCY_UNIT_TYPES

from data_manager.models import FileFeatureSettings


def to_upper_camelcase(value):
    return ''.join(list(map(lambda x: x.title(), value.split('_'))))


def get_excel_file_from_dataframe(df, sheet_name='sheet1'):
    excel_file = IO()
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    writer.save()
    writer.close()
    excel_file.seek(0)

    workbook_encoded = excel_file.getvalue()
    filename = "{sheet_name}-{time}.xlsx".format(
        sheet_name=sheet_name,
        time=str(timezone.now()).replace('.', '::'))

    return workbook_encoded, filename

def get_time_diff_mins(start_time, end_time):
    duration = datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)
    return duration.seconds/60


def get_intervals(parts, duration):
    part_duration = duration / parts
    return [int(i * part_duration) for i in range(parts)]

def get_model_fields(model):
    return list(map(lambda x: x.name, model._meta.fields))


def get_data_and_type_from_excel(file):
    sheet_type = None
    df = pd.read_excel(file)
    df.rename(columns=lambda x: x.strip(), inplace=True)
    if df.columns[0] in ['merchant_code', 'customer_code']:
        sheet_type = df.columns[0].replace('_code', '')
    data = df.to_dict('records')
    return data, sheet_type


def save_excel_data_to_db(data, model):
    create_data_list = list()
    credit_limit_data = dict()
    for single_row_data in data:
        credit_limit_data[single_row_data['customer_code']] = single_row_data.pop('credit_limit')
        create_data_list.append(model(**single_row_data))
    model.objects.bulk_create(create_data_list, batch_size=200)
    return True


def get_model_and_field_list(file_feature_setting, export_type=True):
    model_and_fields = list()
    column_data = file_feature_setting.column_data
    for module_name in column_data.keys():
        model_and_fields += list(map(
            lambda table_name: get_models_and_query_fields(table_name, module_name, column_data, export_type),
            column_data[module_name].keys()))
    return model_and_fields


def get_models_and_query_fields(table_name, module_name, column_data, export_type=True):
    model_name = to_upper_camelcase(table_name)
    model = apps.get_model(module_name, model_name)
    model_fields = get_model_fields(model)

    data_fields = column_data[module_name][table_name]['fields']
    if export_type:
        join_field = column_data[module_name][table_name]['join_field']
        data_fields.append(join_field)
        available_data_fields = list(set(data_fields).intersection(set(model_fields)))
        return {'model': model,
                'fields': available_data_fields,
                'join_field': join_field}
    else:
        concat_field = column_data[module_name][table_name]['concat_field']
        available_data_fields = list(set(data_fields).intersection(set(model_fields)))
        return {'model': model,
                'fields': available_data_fields,
                'concat_field': concat_field}


def get_dataframes_from_settings(file_feature_setting):
    dataframe_list = list()
    model_and_field_list = get_model_and_field_list(file_feature_setting)
    for x in model_and_field_list:
        dataframe_list.append({
            'df': pd.DataFrame(x['model'].objects.values_list(*x['fields']), columns=x['fields']),
            'join_field': x['join_field']
        })
    return dataframe_list


def get_joined_dataframes(file_feature_setting):
    result = get_dataframes_from_settings(file_feature_setting)
    join_fields = [x['join_field'] for x in result]
    # concat all the dataframes with respect to given join fields
    return reduce(
        lambda x, y: x['df'].join(y['df'].set_index(y['join_field']), on=x['join_field']),
        result), join_fields


def export_file_from_settings(file_feature_setting, include_join_fields=False):
    df, join_fields = get_joined_dataframes(file_feature_setting)
    if isinstance(df, dict):
        df = df['df']
    # connection = get_connection()
    if not include_join_fields:
        df.drop([*join_fields], axis=1, errors='ignore', inplace=True)

    excel_file_encoded, file_name = get_excel_file_from_dataframe(df, sheet_name=file_feature_setting.feature_name)
    # connection.create_file_in_remote_location(
    #     excel_file_encoded, file_name, 'EXPORTED')
    return excel_file_encoded


def create_attribute_list_from_column_data(data):
    fields = list()
    idx, column_data = data
    for module in column_data.keys():
        for table in column_data[module].keys():
            fields += column_data[module][table]['fields']
    return {
        'idx': str(idx),
        'fields': fields
    }


def find_most_matched_setting(columns, **kwargs):
    filter_kwargs = kwargs.get('filter_kwargs', {})
    settings_attribute_list = [create_attribute_list_from_column_data(value) for value in
                               FileFeatureSettings.objects.filter(**filter_kwargs).values_list('idx', 'column_data')]

    settings_attribute_list = list(map(lambda x: [
        len(set(x['fields']).intersection(columns)), x
    ], settings_attribute_list))
    most_match_index = max(enumerate(map(itemgetter(0), settings_attribute_list)), key=itemgetter(1))[0]
    feature_settings_idx = settings_attribute_list[most_match_index][1]['idx']
    return FileFeatureSettings.objects.get(idx=feature_settings_idx)


def create_or_update_from_dataframe(model, df, unique_field, insert_type):
    df_copy = df.copy()
    for column in df:
        if hasattr(df[column].astype(str), 'str') and df[column].astype(str).str.match(r'\d{2}/\d{2}/\d{4}').all():
            df_copy[column] = pd.to_datetime(df[column])
    if insert_type == 'update':
        records = df_copy.to_dict('records')
        # TODO: Remove loop and add bulk insert
        for record in records:
            db_record = model.objects.filter(**{unique_field: record[unique_field]}).first()
            if db_record:
                for attr, value in record.items():
                    if isinstance(value, Timestamp):
                        value = make_aware(value)
                    setattr(db_record, attr, value)
                db_record.save()
    elif insert_type == 'create':
        records = df_copy.to_dict('records')
        model_datas = list()
        for record in records:
            model_datas.append(model(**record))
        model.objects.bulk_create(model_datas, batch_size=200)
    return True


@transaction.atomic
def insert_from_model_and_fields_data(df, model_and_fields, insert_type):
    for data in model_and_fields:
        if isinstance(data['concat_field'], dict):
            # create referer dataframe and join with original dataframe
            unique_field_name = data['concat_field']['referer_field']['field']
            referer_values = df[unique_field_name].to_list()
            referer_model = apps.get_model(data['concat_field']['referer_field']['module_name'],
                                           to_upper_camelcase(data['concat_field']['referer_field']['table_name']))
            referer_fields = [
                data['concat_field']['referer_field']['field'],
                data['concat_field']['referer_field']['destination_attribute'],
            ]
            referer_list = referer_model.objects.filter(**{unique_field_name + '__in': referer_values}
                                                        ).values_list(*referer_fields)
            df_referer = pd.DataFrame.from_records(referer_list, columns=referer_fields)
            # type cast unique field to string to avoid error
            df_referer[unique_field_name] = df_referer[unique_field_name].apply(lambda x: str(x))
            df[unique_field_name] = df[unique_field_name].apply(lambda x: str(x))
            df_join = df.join(df_referer.set_index(unique_field_name), on=unique_field_name)

            # create destination dataframe separately and update  fom dataframe
            destination_model = apps.get_model(data['concat_field']['destination_field']['module_name'],
                                               to_upper_camelcase(
                                                   data['concat_field']['destination_field']['table_name']))
            query_field = data['concat_field']['destination_field']['query_field']
            destination_attribute = data['concat_field']['referer_field']['destination_attribute']
            destination_fields = data['fields']
            destination_fields.append(query_field)
            destination_fields = list(set(destination_fields))
            destination_values = df_join[df_join[destination_attribute].notna()][destination_attribute].to_list()
            destination_list = destination_model.objects.filter(**{query_field + '__in': destination_values}
                                                                ).values_list(*destination_fields)
            df_destination = pd.DataFrame.from_records(destination_list, columns=set(destination_fields))
            create_or_update_from_dataframe(destination_model, df_destination, query_field, insert_type)
        else:
            create_or_update_from_dataframe(data['model'], df[data['fields']], data['concat_field'], insert_type)
    return True


def process_create_update_excel_file(file):
    df = pd.read_excel(file)
    columns = df.columns.to_list()
    return_value = True
    # data, sheet_type = get_data_and_type_from_excel(file)
    filter_kwargs = {
        'feature_type__lt': FEATURE_TYPES['EXPORT']
    }
    file_setting = find_most_matched_setting(columns, filter_kwargs=filter_kwargs)
    # get_models_and_query_fields()
    column_data = file_setting.column_data
    model_and_fields = get_model_and_field_list(file_setting, export_type=False)
    main_model_and_field = list(filter(lambda x: not isinstance(x['concat_field'], dict), model_and_fields))[0]
    main_field = main_model_and_field['concat_field']
    main_model = main_model_and_field['model']
    df_values = df[main_field].to_list()
    database_count = main_model.objects.filter(**{main_field+'__in': df_values}).distinct().count()
    insert_type = 'create' if database_count == 0 else None
    if len(df_values) == database_count:
        insert_type = 'update'
    model_and_fields = list(filter(lambda x: not isinstance(x['concat_field'], dict), model_and_fields)
                            ) + list(filter(lambda x: isinstance(x['concat_field'], dict), model_and_fields))
    if insert_type:
        return_value = insert_from_model_and_fields_data(df, model_and_fields, insert_type)
    return return_value


def is_export_time_now(setting, task_interval_in_minutes=1):
    usage_preference = setting.usage_preference
    now = timezone.now().time()
    check_for_time = usage_preference == (FREQUENCY_USAGE_PREFERENCES['TIME'] or
                                          FREQUENCY_USAGE_PREFERENCES['BOTH'] )
    check_for_frequency = usage_preference == (FREQUENCY_USAGE_PREFERENCES['FREQUENCY'] or
                                               FREQUENCY_USAGE_PREFERENCES['BOTH'])
    if check_for_time and setting.generation_time:
        duration = get_time_diff_mins(setting.generation_time, now)
        if task_interval_in_minutes <= duration >= 2 * task_interval_in_minutes:
            return True
    elif check_for_frequency:
        frequency_unit = setting.frequency_unit
        frequency = setting.frequency
        if frequency_unit == FREQUENCY_UNIT_TYPES['HOURLY']:
            export_intervals = get_intervals(frequency, 60)
            for interval in export_intervals:
                start_interval = now.replace(microsecond=0, second=0, minute=interval)
                duration = get_time_diff_mins(start_interval, now)
                if task_interval_in_minutes <= duration >= 2 * task_interval_in_minutes:
                    return True
        elif frequency_unit == FREQUENCY_UNIT_TYPES['DAILY']:
            export_intervals = get_intervals(frequency, 24)
            for interval in export_intervals:
                if timezone.now().hour == interval:
                    start_time = now.replace(microsecond=0, second=0, minute=0)
                    duration = get_time_diff_mins(start_time, now)
                    if task_interval_in_minutes <= duration >= 2 * task_interval_in_minutes:
                        return True
        elif frequency_unit == FREQUENCY_UNIT_TYPES['MONTHLY']:
            export_intervals = get_intervals(frequency, 30)
            for interval in export_intervals:
                if timezone.now().day == interval:
                    start_time = datetime.time(0, 0, 0)
                    duration = get_time_diff_mins(start_time, now)
                    if task_interval_in_minutes <= duration >= 2 * task_interval_in_minutes:
                        return True
    return False
