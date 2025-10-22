# transliterator/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from urllib.parse import unquote
from .converter import AzerbaijaniTransliteration

# Initialize once
transliterator = AzerbaijaniTransliteration()

@require_GET
def convert_text(request):
    # Get and decode URL-encoded parameters
    text = request.GET.get('text', '').strip()
    source = request.GET.get('source', '').lower()
    target = request.GET.get('target', '').lower()

    # URL-decode the text (in case it contains %C9%99 for 'ə', etc.)
    try:
        text = unquote(text)
    except Exception:
        pass  # fallback to raw text

    if not text:
        return JsonResponse({'error': 'Missing "text" parameter'}, status=400)
    if not source or not target:
        return JsonResponse({'error': 'Missing "source" or "target" parameter'}, status=400)

    # Only support Latin → Arabic for now
    if source == 'latin' and target == 'arabic':
        words = text.split()
        arabic_words = [transliterator.transliterate(word) for word in words]
        result = ' '.join(arabic_words)
    else:
        return JsonResponse({
            'error': f'Conversion from "{source}" to "{target}" is not supported yet.'
        }, status=400)

    return JsonResponse({'result': result})