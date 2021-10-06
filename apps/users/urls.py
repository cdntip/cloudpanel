from django.urls import path
from apps.users import views

urlpatterns = [
    path('login', views.Login, name="UserLogin"),
    path('info', views.Info, name="UserInfo"),
]
