from rest_framework.pagination import PageNumberPagination


class FoodgramUserPaginator(PageNumberPagination):
    page_size_query_param = 'limit'

class RecipePaginator(FoodgramUserPaginator):
    pass