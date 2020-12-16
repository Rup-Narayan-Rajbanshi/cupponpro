from django.core.paginator import Paginator

'''A customer class to moke request'''

class Request:
    data = dict()

    def set_data(self, data):
        self.data = data


def custom_paginator(request, queryset, serializer):
    """
    An endpoint for listing all the product categories. Pass 'page' and 'size' as query for requesting particular page and
    number of items per page respectively.
    """
    page_size = request.GET.get('size', None)
    previous_page = None
    next_page = None
    page_count = None
    if page_size and page_size.isnumeric():
        page_number = request.GET.get('page')
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)
        if page_obj.has_previous():
            previous_page = page_obj.previous_page_number()
        else:
            previous_page = None
            if page_obj.has_next():
                next_page = page_obj.next_page_number()
            else:
                next_page = None
        queryset = page_obj
    serializers = serializer(queryset, many=True,\
        context={"request":request})
    data = {
        'success': 1,
        'previous_page': previous_page,
        'next_page': next_page,
        'page_count': page_count,
        'data': serializers.data,
    }
    return data
