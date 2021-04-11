from django.urls import include, path
from . import views

urlpatterns = [
    path("login/", views.login, name='login'),
    path("create/", views.create_user, name='create_user'),
]