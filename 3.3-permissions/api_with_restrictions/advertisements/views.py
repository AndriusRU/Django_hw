from _ast import Add

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Advertisement, AdvertisementStatusChoices, AdvertisementFavorite
from .serializers import AdvertisementSerializer, AdvertisementFavoriteSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrAdmin, IsDraft, AddFavorite


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    # pagination_class = PageNumberPagination
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        set1 = super().get_queryset().exclude(status=AdvertisementStatusChoices.DRAFT)
        if not user.is_anonymous:
            return set1.union(Advertisement.objects.all().filter(status=AdvertisementStatusChoices.DRAFT, creator=user))
        return set1


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return []

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # if IsOwnerOrAdmin():
    #     queryset = queryset.exclude(status=AdvertisementStatusChoices.DRAFT)
    #
    #     result = self.get_serializer(queryset, many=True)
    #     return Response(result.data)


class AdvertisementFavoriteViewSet(ModelViewSet):
    serializer_class = AdvertisementFavoriteSerializer
    permission_classes = [AddFavorite]
    filter_backends = [DjangoFilterBackend]
    queryset = AdvertisementFavorite.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated(), AddFavorite()]
        return []
