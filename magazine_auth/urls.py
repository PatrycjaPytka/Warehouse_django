from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView

from . import views


app_name = "magazine_auth"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='auth'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]