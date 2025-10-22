from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_words, name='all-words'),
    path('search/', views.search_words, name='search-words'),
    path('<str:word>/', views.word_detail, name='word-detail'),
]