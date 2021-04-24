from django.urls import include, path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('home/', views.index, name='home'),
]