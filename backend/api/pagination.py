from rest_framework.pagination import PageNumberPagination


class NumberRecordsPerPagePagination(PageNumberPagination):
    """Пагинация по количеству выдаваемых записей на страницу, которую может
    устанавливать пользователь."""

    page_size = 6
    page_size_query_param = 'limit'
