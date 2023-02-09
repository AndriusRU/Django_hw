from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import AdvertisementStatusChoices, Advertisement


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' or request.user.is_staff:
            return True
        return obj.creator == request.user


# Просмотр Draft объявлений
class IsDraft(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user.is_staff or obj.creator == request.user:
            return True

        if obj.status == AdvertisementStatusChoices.DRAFT and request.user == obj.creator:
            return True

        if obj.status != AdvertisementStatusChoices.DRAFT and request.method in SAFE_METHODS:
            return True

        return False


class AddFavorite(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user != Advertisement.get_queryset().filter(id=obj.adv).creator or request.user.is_staff:
            return True

        return False
