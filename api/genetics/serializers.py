# serializers.py

from rest_framework import serializers
from .models import GeneticSample, HistoricalPeriod


class HistoricalPeriodSerializer(serializers.ModelSerializer):
    display = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = HistoricalPeriod
        fields = ('name', 'start_year', 'end_year', 'display')


class GeneticSampleSerializer(serializers.ModelSerializer):
    # Direct flat string fields from foreign keys
    country = serializers.CharField(source='country.name', allow_null=True)
    province = serializers.CharField(source='province.name', allow_null=True)
    city = serializers.CharField(source='city.name', allow_null=True)

    y_dna = serializers.SerializerMethodField()
    mt_dna = serializers.SerializerMethodField()
    historical_period = HistoricalPeriodSerializer()

    class Meta:
        model = GeneticSample
        fields = (
            'name',
            'country',
            'province',
            'city',
            'y_dna',
            'mt_dna',
            'historical_period',
            'description'
        )

    def get_y_dna(self, obj):
        if obj.y_dna:
            return {
                'name': obj.y_dna.name,
                'root_haplogroup': obj.y_dna.get_root_haplogroup(),
            }
        return None

    def get_mt_dna(self, obj):
        if obj.mt_dna:
            return {
                'name': obj.mt_dna.name,
                'root_haplogroup': obj.mt_dna.get_root_haplogroup(),
            }
        return None