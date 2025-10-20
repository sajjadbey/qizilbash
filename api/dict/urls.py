from django.urls import path
from . import views

urlpatterns = [
    path('dict/all/', views.all_words, name='all-words'),
    path('dict/<str:word>/', views.word_detail, name='word-detail'),
    path('search/', views.search_words, name='search-words'),
]