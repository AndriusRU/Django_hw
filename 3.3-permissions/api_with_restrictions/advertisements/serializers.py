from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Advertisement, AdvertisementStatusChoices, AdvertisementFavorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementFavoriteSerializer(serializers.ModelSerializer):
    """Serializer для избранных объявлений."""

    user = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = AdvertisementFavorite
        fields = ('adv', 'user')

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        if Advertisement.get_queryset().filter(id=data.get('adv')).creator == self.context["request"].user:
            raise ValidationError('Добавить в избранное можно только чужое объявление !')
        return data


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        count_open_adv = self.Meta.model.objects.filter(
            creator=self.context["request"].user,
            status=AdvertisementStatusChoices.OPEN
        ).count()

        if count_open_adv > 9 and self.context["request"].method == "POST" or \
                (self.context["request"].method == "PATCH" and data.get('status') == "OPEN"):
            raise ValidationError('Открытых объявлений не может быть больше 10')
        return data

