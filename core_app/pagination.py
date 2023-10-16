from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class MetaPageNumberPagination(PageNumberPagination):
    page = 1
    page_size = 10
    page_size_query_param = 'per_page'

    def get_from(self):
        return int((self.page.paginator.per_page * self.page.number) - self.page.paginator.per_page + 1)

    def get_to(self):
        return self.get_from() + len(self.page.object_list) - 1

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': "Records fetched successfully",
            'meta': {
                'total': self.page.paginator.count,
                'current_page': int(self.request.GET.get('page', MetaPageNumberPagination.page)),
                'next_page_url': self.get_next_link(),
                'previous_page_url': self.get_previous_link(),
                'page_size': int(self.request.GET.get('per-page', self.page_size)),
                'last_page': self.page.paginator.num_pages,
            },
            'data': data
        })
