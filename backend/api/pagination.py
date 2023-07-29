from rest_framework.pagination import PageNumberPagination
from foodgram.settings import PAGE_SIZE
from django.core.paginator import Paginator


class LimitPagePagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'limit'
    page_query_param = 'page'
    django_paginator_class = Paginator
