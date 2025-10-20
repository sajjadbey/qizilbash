from rest_framework import serializers
from .models import Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id',
            'word',
            'english_translation',
            'persian_translation',
            'meaning_english',
            'meaning_azerbaijani',
            'word_type',
            'created_at'
        ]