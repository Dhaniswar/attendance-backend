from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # Items per page
    page_size_query_param = 'page_size'  # Allow client to override page size
    max_page_size = 100  # Maximum page size