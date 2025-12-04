# views.py

from rest_framework import generics
from .models import GeneticSample
from .serializers import GeneticSampleSerializer

class SampleListView(generics.ListAPIView):
    queryset = GeneticSample.objects.select_related(
        'city__province__country',
        'y_dna',
        'mt_dna',
        'historical_period'
    ).all()
    serializer_class = GeneticSampleSerializer
    pagination_class = None  # remove if you want pagination