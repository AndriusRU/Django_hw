import django_filters
import django_filters as filters
from .models import Stock, Product, StockProduct

class FilterStock(filters.FilterSet):
    products__title = django_filters.CharFilter(lookup_expr='icontains')
    # products__description = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Stock
        fields = {'products'}

