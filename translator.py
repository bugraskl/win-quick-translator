"""Google Translate API wrapper with smart language detection."""

from googletrans import Translator


class TranslationService:
    """Handles translation requests using Google Translate."""
    
    def __init__(self, primary_language: str = 'tr'):
        self.translator = Translator()
        self.primary_language = primary_language
    
    def translate(self, text: str) -> dict:
        """
        Translate text with smart language detection.
        - If source is primary_language → translate to English
        - If source is NOT primary_language → translate to primary_language
        
        Returns:
            dict with translated text and metadata
        """
        if not text or not text.strip():
            return {
                'translated': '',
                'source_lang': '',
                'target_lang': '',
                'detected_lang': '',
                'success': False,
                'error': 'Empty text'
            }
        
        try:
            # First, detect the language
            detected = self.translator.detect(text)
            detected_lang = detected.lang if detected else 'en'
            
            # Smart target selection
            if detected_lang == self.primary_language:
                target_lang = 'en'
            else:
                target_lang = self.primary_language
            
            # Perform translation
            result = self.translator.translate(
                text,
                src=detected_lang,
                dest=target_lang
            )
            
            return {
                'translated': result.text,
                'source_lang': detected_lang,
                'target_lang': target_lang,
                'detected_lang': detected_lang,
                'success': True,
                'error': None
            }
        except Exception as e:
            return {
                'translated': '',
                'source_lang': '',
                'target_lang': '',
                'detected_lang': '',
                'success': False,
                'error': str(e)
            }
    
    def get_language_name(self, code: str) -> str:
        """Convert language code to Turkish name."""
        languages = {
            'en': 'İngilizce',
            'tr': 'Türkçe',
            'de': 'Almanca',
            'fr': 'Fransızca',
            'es': 'İspanyolca',
            'it': 'İtalyanca',
            'ru': 'Rusça',
            'ar': 'Arapça',
            'zh-cn': 'Çince',
            'zh-tw': 'Çince',
            'ja': 'Japonca',
            'ko': 'Korece',
            'pt': 'Portekizce',
            'nl': 'Hollandaca',
            'pl': 'Lehçe',
            'sv': 'İsveççe',
            'da': 'Danca',
            'fi': 'Fince',
            'no': 'Norveççe',
            'el': 'Yunanca',
            'cs': 'Çekçe',
            'hu': 'Macarca',
            'ro': 'Rumence',
            'uk': 'Ukraynaca',
            'ms': 'Malayca',
        }
        return languages.get(code, code.upper())
