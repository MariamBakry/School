from rest_framework.pagination import CursorPagination

"""
    Custom cursor-based pagination class.

    Provides pagination using cursors for efficient retrieval of large datasets.

    **Attributes:**
        page_size (int): The number of items per page. Defaults to 3.
        ordering (str): The field used for ordering results. Defaults to '-id'
    """
class CustomCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-id'