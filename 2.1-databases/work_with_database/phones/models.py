from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.TextField()
    release_date = models.DateField(max_length=10)
    lte_exists = models.BooleanField()
    slug = models.SlugField(blank=True, unique=True, verbose_name='url')



