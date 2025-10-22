# converter.py

import re

class AzerbaijaniTransliteration:
    """
    A class for transliterating Azerbaijani Latin script to a customized 
    Arabic script, focusing on positional rules for short vowels.

    The short vowels (ə, e, o) are mapped to Harakat (diacritical marks) 
    in the medial position, and to specific letters (ه or و) in the final position.
    """

    # --- Arabic Vowel Marks (Harakat) ---
    FATHA = 'َ' # Used for 'ə' (Fatha: /a/ or /æ/)
    KASRA = 'ِ' # Used for 'e' (Kasra: /i/ or /e/)
    DAMMA = 'ُ' # Used for 'o' (Damma: /u/ or /o/)
    
    # --- Final Vowel Characters ---
    HEH_FINAL = 'ه' # Used for final 'ə', 'e'
    WAW_FINAL = 'و' # Used for final 'o'

    # --- Base Mappings for Consonants and Long Vowels (Standalone Letters) ---
    MAPPINGS = {
        # Long Vowels / Semi-Vowels (Waw, Ya, Alif)
        'a': 'ا', 'i': 'ي', 'ı': 'ى', 'u': 'و', 'ü': 'و',
        'ö': 'ۆ', # Specific letter for 'ö'
        'v': 'و', # Consonant 'v'
        'y': 'ی', # Consonant 'y'

        # Consonants
        'b': 'ب', 'c': 'ج', 'ç': 'چ', 'd': 'د', 'f': 'ف',
        'g': 'گ', 'ğ': 'غ', 'h': 'ح', 'x': 'خ', 'j': 'ژ',
        'k': 'ك', 'q': 'ق', 'l': 'ل', 'm': 'م', 'n': 'ن',
        'p': 'پ', 'r': 'ر', 's': 'س', 'ş': 'ش', 't': 'ت',
        'z': 'ز',
    }

    # Positional Short Vowels to be handled with Harakat (marks)
    POSITIONAL_VOWELS = {'ə': FATHA, 'e': KASRA, 'o': DAMMA}

    def transliterate(self, word: str) -> str:
        """
        Transliterates a single Azerbaijani Latin word to the Arabic script.

        Args:
            word: The Azerbaijani Latin word to transliterate.

        Returns:
            The transliterated Arabic script string.
        """
        
        # Prepare input
        word = word.lower()
        arabic_chars = [] # Output buffer
        
        # ----------------------------------------------------
        # --- Iterative Transliteration and Harakat Application ---
        # ----------------------------------------------------
        
        for i, char in enumerate(word):
            is_last = (i == len(word) - 1)
            
            if char in self.MAPPINGS:
                # 1. Consonants and Long Vowels: Add the Arabic base letter
                arabic_chars.append(self.MAPPINGS[char])

            elif char in self.POSITIONAL_VOWELS:
                # 2. Positional Short Vowels (ə, e, o)
                
                if is_last:
                    # Rule: Final 'o' maps to WAW, final 'ə'/'e' maps to HEH
                    if char == 'o':
                        arabic_chars.append(self.WAW_FINAL)
                    else:
                        arabic_chars.append(self.HEH_FINAL)
                
                else:
                    # Rule: In the middle of a word, apply Harakat (mark) to the previous consonant.
                    mark = self.POSITIONAL_VOWELS[char]
                    
                    if arabic_chars:
                        # Append the Harakat (vowel mark) right after the consonant it modifies.
                        arabic_chars.append(mark)
                    else:
                        # If it's the very first letter (word-initial short vowel), 
                        # use Alif (ا) as a placeholder for the mark to sit on.
                        arabic_chars.append('ا')
                        arabic_chars.append(mark)

            else:
                # Handle unknown characters
                arabic_chars.append(char)

        return "".join(arabic_chars)
