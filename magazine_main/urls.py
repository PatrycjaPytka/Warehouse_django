from django.urls import path

from . import views


app_name = "magazine_main"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('manage/', views.ManageWarehouseView.as_view(), name='manage_warehouse'),
    path('manage/items_list/', views.ItemsList.as_view(), name='items_list'),
    path('manage/users_list/', views.UsersList.as_view(), name='users_list'),
    path('manage/borrowed_user_list/<int:pk>/', views.BorrowedUserList.as_view(), name='borrowed_user_list'),
    path('manage/<int:pk>/<str:action>/', views.ManageWarehouseAction.as_view(), name='manage_action'),
]