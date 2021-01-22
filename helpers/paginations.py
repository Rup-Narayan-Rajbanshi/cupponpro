from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import InvalidPage


class FPagination(PageNumberPagination):
	"""
	Pagination class.
	"""

	page_size = 10
	page_size_query_param = "page_size"
	max_page_size = 100

	def paginate_queryset(self, queryset, request, view=None):
		"""
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
		page_size = self.get_page_size(request)
		if not page_size:
			return None

		paginator = self.django_paginator_class(queryset, page_size)
		page_number = request.query_params.get(self.page_query_param, 1)
		if page_number in self.last_page_strings:
			page_number = paginator.num_pages

		try:
			self.page = paginator.page(page_number)
		except InvalidPage as exc:
			try:
				page_number = 1 if int(page_number) < 1 else paginator.num_pages
				self.page = paginator.page(page_number)
			except:
				self.page = paginator.page(1)


		if paginator.num_pages > 1 and self.template is not None:
			# The browsable API should display pagination controls.
			self.display_page_controls = True

		self.request = request
		return list(self.page)

	def get_paginated_response(self, data):
		"""
		API response data.
		"""

		return Response(OrderedDict([
			('total_pages', self.page.paginator.num_pages),
			('total_records', self.page.paginator.count),
			('next', self.get_next_page()),
			('previous', self.get_prev_page()),
			('record_range', self.get_record_range()),
			('current_page', self.page.number),
			('records', data)
		]))

	def get_record_range(self):
		"""
		Range of contents in current page.
		"""

		paginator = self.page.paginator
		current_page = self.page.number
		content_per_page = paginator.per_page

		if paginator.count == 0:
			range_start = 0
			range_end = 0
		else:
			range_start = content_per_page * (current_page - 1) + 1
			range_end = content_per_page * current_page

		if range_end > paginator.count:
			range_end = paginator.count

		return [range_start, range_end]

	def get_next_page(self):
		if not self.page.has_next():
			return None
		return str(self.page.next_page_number())


	def get_prev_page(self):
		if not self.page.has_previous():
			return None
		return str(self.page.previous_page_number())

class FMaxPagination(PageNumberPagination):
	"""
	Pagination class.
	"""

	page_size = 50
	page_size_query_param = "page_size"
	max_page_size = 200

	def get_paginated_response(self, data):
		"""
		API response data.
		"""

		return Response(OrderedDict([
			('total_pages', self.page.paginator.num_pages),
			('total_records', self.page.paginator.count),
			('next', self.get_next_link()),
			('previous', self.get_previous_link()),
			('record_range', self.get_record_range()),
			('current_page', self.page.number),
			('records', data)
		]))

	def get_record_range(self):
		"""
		Range of contents in current page.
		"""

		paginator = self.page.paginator
		current_page = self.page.number
		content_per_page = paginator.per_page

		if paginator.count == 0:
			range_start = 0
			range_end = 0
		else:
			range_start = content_per_page * (current_page - 1) + 1
			range_end = content_per_page * current_page

		if range_end > paginator.count:
			range_end = paginator.count

		return [range_start, range_end]
