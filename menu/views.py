from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from .models import Category, Dish
from .serializers import CategorySerializer, CategoryListSerializer


class CategoryAPIView(ListAPIView):
    queryset = Category.objects.filter(is_active=True, parent__isnull=True).order_by('order')
    serializer_class = CategoryListSerializer


class MenuAPIView(ListAPIView):
    queryset = Category.objects.prefetch_related(
        'dishes').filter(is_active=True, parent__isnull=True).order_by('order')
    serializer_class = CategorySerializer


def index(request):
    return render(request, 'index.html')


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    dishes = category.dishes.all().order_by('order')
    subcategories = category.subcategories.filter(is_active=True).order_by('order')
    return render(request, 'category_detail.html', {
        'category': category,
        'dishes': dishes,
        'subcategories': subcategories
    })


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, 'dish_detail.html', {'dish': dish})
