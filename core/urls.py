from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from menu.views import MenuAPIView, index, CategoryAPIView, category_detail, dish_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/menu/', MenuAPIView.as_view()),
    path('api/category/', CategoryAPIView.as_view()),
    path('', index, name='index'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('dish/<int:dish_id>/', dish_detail, name='dish_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
