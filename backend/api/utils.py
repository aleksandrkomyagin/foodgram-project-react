from rest_framework import mixins, viewsets


class ListRetrieveVeiwSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass
