from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name='Название')
    order = models.PositiveIntegerField(
        default=0, verbose_name='Место на странице')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Dish(models.Model):
    category = models.ForeignKey(
        Category, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=120, verbose_name='Название')
    image = models.FileField(
        upload_to='dish_images/',
        validators=[
            FileExtensionValidator(allowed_extensions=[
                                   'jpg', 'jpeg', 'png', 'webp', 'svg'])
        ],
        verbose_name='Фото блюда',
        blank=True,
        null=True
    )
    weight = models.CharField(max_length=10, verbose_name='Грамовка')
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Цена')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
