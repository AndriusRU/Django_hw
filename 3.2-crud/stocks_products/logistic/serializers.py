from rest_framework import serializers
from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for elem in positions:
            new_stock_product = StockProduct.objects.create(
                product=elem['product'],
                stock=stock,
                quantity=elem['quantity'],
                price=elem['price']
            )
            stock.positions.add(new_stock_product)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for elem in positions:
            StockProduct.objects().update_or_create(
                stock=stock,
                product=elem['product'],
                defaults={
                    'quantity': elem['quantity'],
                    'price': elem['price']
                }
            )

        return stock

    class Meta:
        model = Stock
        fields = ['address', 'positions']
