from django.contrib import admin
from .models import Word

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'word_type', 'created_at')
    search_fields = ('word', 'english_translation', 'meaning_azerbaijani')
    list_filter = ('word_type',)