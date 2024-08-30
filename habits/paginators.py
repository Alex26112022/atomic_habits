from rest_framework.pagination import PageNumberPagination


class MyPaginator(PageNumberPagination):
    """ Постраничный вывод. """
    page_size = 5
