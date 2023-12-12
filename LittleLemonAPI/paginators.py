from rest_framework import pagination

class MenuPagination(pagination.PageNumberPagination):
    page_size = 10