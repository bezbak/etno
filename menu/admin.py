from django.contrib import admin
from .models import Category, Dish
from django.core.files.base import ContentFile
import os

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    actions = ["duplicate_category"]

    def duplicate_category(self, request, queryset):
        for category in queryset:
            # копируем категорию
            category_copy = Category.objects.create(
                name=f"{category.name} (копия)",
                order=category.order
            )

            # копируем все блюда категории
            for dish in category.dishes.all():
                Dish.objects.create(
                    category=category_copy,
                    name=dish.name,
                    description=dish.description,
                    price=dish.price,
                    weight=dish.weight,
                    image=dish.image,
                    is_available=dish.is_available,
                )

        self.message_user(request, "Категории успешно скопированы")

    duplicate_category.short_description = "Скопировать категорию с блюдами"


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    actions = ["duplicate_dish", "resave_images"]

    def duplicate_dish(self, request, queryset):
        for dish in queryset:
            Dish.objects.create(
                category=dish.category,
                name=f"{dish.name} (копия)",
                description=dish.description,
                price=dish.price,
                weight=dish.weight,
                image=dish.image,
                is_available=dish.is_available,
            )

        self.message_user(request, "Блюда успешно скопированы")

    duplicate_dish.short_description = "Скопировать блюдо"

    def resave_images(self, request, queryset):
        updated = 0

        for dish in queryset:
            if not dish.image:
                continue

            ext = os.path.splitext(dish.image.name)[1].lower()

            # SVG и уже WebP не трогаем
            if ext in [".webp", ".svg"]:
                continue

            # КЛЮЧЕВО: переустанавливаем файл, чтобы сработал save()
            dish.image = dish.image
            dish.save()
            updated += 1

        self.message_user(
            request,
            f"Пересохранено изображений: {updated}"
        )

    resave_images.short_description = "Пересохранить фото (JPG → WebP)"