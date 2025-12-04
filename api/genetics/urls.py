# urls.py (in your genetics app)

from django.urls import path
from . import views

app_name = 'genetics'

urlpatterns = [
    path('samples/', views.SampleListView.as_view(), name='sample-list'),
]