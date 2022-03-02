from django.urls import path

from . import views


app_name = "magazine_main"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('manage/', views.ManageWarehouseView.as_view(), name='manage_warehouse'),
    path('manage/items_list', views.ItemsList.as_view(), name='items_list')
]