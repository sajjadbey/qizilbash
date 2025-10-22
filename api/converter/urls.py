# transliterator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert_text, name='convert-text'),
]