from collections import OrderedDict

import operator
from functools import reduce

from dateutil import parser
from django.db import models
from django.db.models import Q
from django_filters import filters

from django_filters.filterset import (
    FILTER_FOR_DBFIELD_DEFAULTS,
    FilterSet,
)
from django_filters.filterset import remote_queryset
from django_filters.filters import ModelChoiceFilter
from django_filters.rest_framework import DjangoFilterBackend


FILTER_FOR_DBFIELD_DEFAULTS[models.OneToOneField] = {
    'filter_class': ModelChoiceFilter,
    'extra': lambda f: {
        'queryset': remote_queryset(f),
        'to_field_name': "idx",
    }
}

FILTER_FOR_DBFIELD_DEFAULTS[models.ForeignKey] = {
    'filter_class': ModelChoiceFilter,
    'extra': lambda f: {
        'queryset': remote_queryset(f),
        'to_field_name': "idx",
    }
}


class KFilterSet(FilterSet):
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS


class KDjangoFilterBackend(DjangoFilterBackend):
    default_filter_set = KFilterSet


def filter_boolean(queryset, name, value):
    m = {"true": True, "false": False}
    filter = {name: m.get(value)}
    return queryset.filter(**filter)


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CustomDateRangeFilterMixin:

    date_range_alias = {
        'start_datetime': None,
        'end_datetime': None
    }

    def custom_date_range_filter(self, qs, start_datetime, end_datetime):
        start_datetime_field = self.date_range_alias['start_datetime']
        end_datetime_field = self.date_range_alias['end_datetime']

        return qs.filter(
            Q(
                Q(
                    **{
                        '{}__lte'.format(start_datetime_field): start_datetime,
                        '{}__gte'.format(end_datetime_field): start_datetime
                    }
                ) & Q(
                    **{
                        '{}__lte'.format(start_datetime_field): end_datetime,
                        '{}__gte'.format(end_datetime_field): end_datetime
                    }
                )
            ) | Q(
                **{
                    '{}__gte'.format(start_datetime_field): start_datetime,
                    '{}__lte'.format(end_datetime_field): end_datetime
                }
            ) | Q(
                **{
                    '{}__gte'.format(start_datetime_field): start_datetime,
                    '{}__gte'.format(end_datetime_field): end_datetime,
                    '{}__lte'.format(start_datetime_field): end_datetime
                }
            ) | Q(
                **{
                    '{}__lte'.format(start_datetime_field): start_datetime,
                    '{}__lte'.format(end_datetime_field): end_datetime,
                    '{}__gte'.format(end_datetime_field): start_datetime
                }
            )
        )

    @property
    def qs(self):
        qs = super().qs
        start_time, end_time = self.request.GET.get(self.date_range_alias['start_datetime']), self.request.GET.get(self.date_range_alias['end_datetime'])
        try:
            if start_time is not None and end_time is not None:
                start_time, end_time = parser.parse(start_time), parser.parse(end_time)
                qs = self.custom_date_range_filter(qs, start_time, end_time)
        except Exception:
            pass

        return qs


class CustomOrderingFilterMixin:
    ordering_map = OrderedDict([
        ('asc', ''),
        ('desc', '-')
    ])

    ordering_fields = OrderedDict([])

    @property
    def qs(self):
        qs = super().qs

        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by is not None and order_by in self.ordering_fields.keys():
            if ordering is not None and ordering in self.ordering_map.keys():
                if isinstance(self.ordering_fields[order_by], list):
                    if ordering == 'desc':
                        qs = qs.order_by(*self.ordering_fields[order_by]).reverse()
                    else:
                        qs = qs.order_by(*self.ordering_fields[order_by])

                else:
                    order_lookup = '{}{}'.format(
                        self.ordering_map[ordering],
                        self.ordering_fields[order_by]
                    )
                    qs = qs.order_by(order_lookup)

            else:
                if isinstance(self.ordering_fields[order_by], list):
                    qs = qs.order_by(*self.ordering_fields[order_by])
                else:
                    order_lookup = self.ordering_fields[order_by]
                    qs = qs.order_by(order_lookup)

        else:
            prior_ordering_field = list(self.ordering_fields.keys())[0]
            prior_ordering = list(self.ordering_map.keys())[0]
            if isinstance(self.ordering_fields[prior_ordering_field], list):
                if ordering == 'desc':
                    qs = qs.order_by(*self.ordering_fields[prior_ordering_field]).reverse()
                else:
                    qs = qs.order_by(*self.ordering_fields[prior_ordering_field])

            else:
                order_lookup = '{}{}'.format(
                    self.ordering_map[prior_ordering],
                    self.ordering_fields[prior_ordering_field]
                )
                qs = qs.order_by(order_lookup)
        return qs


class ORFilterMixin:

    default_lookup = 'iexact'
    lookups = ['in', 'icontains']

    def fields_with_lookup(self):
        fields = []
        for field in self.Meta.fields:
            fields.append(field)
            fields += ['{}__{}'.format(field, lookup) for lookup in self.lookups]

        return fields

    def or_qs(self):
        if 'operation' in self.request.GET:
            if self.request.GET['operation'] == 'or':
                query_params = self.request.GET
                filter_expression = []
                for field in self.fields_with_lookup():
                    if field in query_params:
                        value = query_params[field].split(',') if field.endswith('__in') else query_params[field]
                        if field.find('__') < 0:
                            field = '{}__{}'.format(field, self.default_lookup)
                        filter_expression.append(Q(**{'{}'.format(field): value}))

                if filter_expression:
                    parent = self.Meta.model.objects.filter(reduce(operator.or_, filter_expression))
                    return parent

        parent = super().qs
        return parent
