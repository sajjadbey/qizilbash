from django.db import models

# Create your models here.
from django.db import models

WORD_TYPES = [
    ('noun', 'Noun'),
    ('verb', 'Verb'),
    ('adjective', 'Adjective'),
    ('adverb', 'Adverb'),
    ('pronoun', 'Pronoun'),
    ('preposition', 'Preposition'),
    ('conjunction', 'Conjunction'),
    ('interjection', 'Interjection'),
    ('other', 'Other'),
]

class Word(models.Model):
    word = models.CharField(max_length=255, unique=True, db_index=True)
    english_translation = models.TextField(blank=True)
    persian_translation = models.TextField(blank=True)
    meaning_english = models.TextField(blank=True)
    meaning_azerbaijani = models.TextField(blank=True)
    word_type = models.CharField(max_length=20, choices=WORD_TYPES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ['word']