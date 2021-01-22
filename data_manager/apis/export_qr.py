import xlwt
import shortuuid
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from commonapp.models.asset import Asset
from permission import isAdmin


@api_view(["GET"])
@permission_classes((isAdmin,))
def export_company_qr(request):
    response = HttpResponse(content_type='application/ms-excel')
    random_name = shortuuid.ShortUUID().random(length=6)
    name = 'QR-{0}.xls'.format(random_name)
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(name)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('QR')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['S. No.', 'Link', 'Table No.', 'Merchant Name', 'Merchant Code']
    col_lengths = []

    for col_num in range(len(columns)):
        # if col_num == 1:
        #     font_style.
        ws.write(row_num, col_num, columns[col_num], font_style)
        col_lengths.append(len(columns[col_num]))
    col_lengths[1] = 103
    # Sheet body, remaining rows
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    font_style = xlwt.XFStyle()
    font_style.alignment = alignment
    rows = Asset.objects.select_related('company').all().values_list('id', 'company', 'name', 'company__name', 'company__key')
    for row in rows:
        row_num += 1
        link_text = 'https://mastarqr.com/{0}?table_no={1}'.format(row[1], row[0])
        # for col_num in range(len(row)):
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, link_text, font_style)
        ws.write(row_num, 2, row[2], font_style)
        ws.write(row_num, 3, row[3], font_style)
        ws.write(row_num, 4, row[4], font_style)
        for i in range(len(columns)):
            if i > 0:
                row_len = len(str(row[i]))
                if col_lengths[i] < row_len:
                    col_lengths[i] = row_len
    for col in range(len(col_lengths)):
        if col > 0:
            col_length = col_lengths[col]
            link_col = ws.col(col)
            link_col.width = 256 * (col_length + 1)
    wb.save(response)
    return response
