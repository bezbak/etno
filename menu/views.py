from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer


class MenuAPIView(ListAPIView):
    queryset = Category.objects.prefetch_related('dishes').order_by('order')
    serializer_class = CategorySerializer
    
def index(request):
    return render(request, 'index.html')