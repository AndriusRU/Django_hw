from django_filters import rest_framework as filters, DateTimeFromToRangeFilter

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = DateTimeFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ["creator", "created_at", "status"]
