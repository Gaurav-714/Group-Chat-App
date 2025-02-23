from django.urls import path
from .views import home

urlpatterns = [
    path('<str:group_name>/', home),
]
