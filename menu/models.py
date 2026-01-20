from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile
from PIL import Image
import io
import os
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

    def save(self, *args, **kwargs):
        if self.image:
            ext = os.path.splitext(self.image.name)[1].lower()

            # SVG не трогаем
            if ext in ['.jpg', '.jpeg', '.png']:
                img = Image.open(self.image)
                img = img.convert("RGB")

                buffer = io.BytesIO()
                img.save(
                    buffer,
                    format="WEBP",
                    quality=80,      # оптимальный баланс
                    method=6         # максимальное сжатие
                )

                webp_name = os.path.splitext(self.image.name)[0] + '.webp'
                self.image.save(
                    webp_name,
                    ContentFile(buffer.getvalue()),
                    save=False
                )

        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
