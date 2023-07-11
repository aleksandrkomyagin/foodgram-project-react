from rest_framework import viewsets, mixins


class GetPostUserViewSet(
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    http_method_names = ('get', 'post',)
