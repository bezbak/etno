from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from .models import Category, Dish
from .serializers import CategorySerializer, CategoryListSerializer


class CategoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class MenuAPIView(ListAPIView):
    queryset = Category.objects.prefetch_related('dishes').order_by('order')
    serializer_class = CategorySerializer


def index(request):
    return render(request, 'index.html')

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    dishes = category.dishes.all()
    return render(request, 'category_detail.html', {
        'category': category,
        'dishes': dishes
    })


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, 'dish_detail.html', {'dish': dish})