from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('createURL', views.createURL),
    path('<str:alias>', views.findURL),
]