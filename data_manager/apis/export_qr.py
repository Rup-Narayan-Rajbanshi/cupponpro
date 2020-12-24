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
    name = 'QR-{0}.xlsx'.format(random_name)
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(name)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('QR')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['S. No.', 'Link']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Asset.objects.all().values_list('id', 'company')
    for row in rows:
        row_num += 1
        link_text = 'https://mastarqr.com/{0}?table_no={1}'.format(row[1], row[0])
        # for col_num in range(len(row)):
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, link_text, font_style)

    wb.save(response)
    return response
