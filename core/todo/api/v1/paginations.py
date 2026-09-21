from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class TaskPagination(PageNumberPagination):
    page_size = 2
    def get_paginated_response(self, data):
        return Response(
            data={
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                },
                'count': self.page.paginator.count,
                'results': data,
            }
        )