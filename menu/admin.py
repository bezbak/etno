from django.contrib import admin
from django.db.models import Q
from .models import Category, Dish
import os


class HasImageFilter(admin.SimpleListFilter):
    title = "Наличие фото"
    parameter_name = "has_image"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Есть фото"),
            ("no", "Нет фото"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(Q(image="") | Q(image__isnull=True))
        if self.value() == "no":
            return queryset.filter(Q(image="") | Q(image__isnull=True))
        return queryset


class SubcategoryInline(admin.TabularInline):
    model = Category
    fk_name = 'parent'
    fields = ('name', 'order', 'is_active')
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "get_is_active")
    list_filter = ("is_active",)
    actions = ["duplicate_category",
               "activate_categories", "deactivate_categories"]
    inlines = [SubcategoryInline]

    def get_is_active(self, obj):
        return obj.is_active
    get_is_active.boolean = True
    get_is_active.short_description = "Активна"

    def get_inline_instances(self, request, obj=None):
        # Показываем инлайн только если есть дочерние категории
        if obj is None or not obj.subcategories.exists():
            return []
        return super().get_inline_instances(request, obj)

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

    def activate_categories(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Активировано категорий: {updated}")

    activate_categories.short_description = "✅ Включить выбранные категории"

    def deactivate_categories(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Деактивировано категорий: {updated}")

    deactivate_categories.short_description = "❌ Выключить выбранные категории"


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "get_is_available")
    search_fields = ("name", "description")   # 🔍 поиск
    list_filter = ("category", "is_available", HasImageFilter)  # 🧩 фильтры
    actions = ["duplicate_dish", "resave_images",
               "make_available", "make_unavailable"]

    def get_is_available(self, obj):
        return obj.is_available
    get_is_available.boolean = True
    get_is_available.short_description = "Доступно"

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

    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f"Доступно блюд: {updated}")

    make_available.short_description = "✅ Сделать доступными"

    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f"Недоступно блюд: {updated}")

    make_unavailable.short_description = "❌ Сделать недоступными"
