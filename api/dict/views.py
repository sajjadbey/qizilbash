from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Word
from .serializers import WordSerializer

@api_view(['GET'])
def all_words(request):
    words = Word.objects.all()
    serializer = WordSerializer(words, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def word_detail(request, word):
    """Get word by Azerbaijani spelling: /api/dictionary/salam"""
    word_obj = get_object_or_404(Word, word__iexact=word)
    serializer = WordSerializer(word_obj)
    return Response(serializer.data)

@api_view(['GET'])
def search_words(request):
    """Search words: /api/search?text=salam"""
    query = request.GET.get('text', '').strip()
    if not query:
        return Response({"error": "Missing 'text' parameter"}, status=status.HTTP_400_BAD_REQUEST)

    words = Word.objects.filter(word__icontains=query)
    serializer = WordSerializer(words, many=True)
    return Response(serializer.data)

