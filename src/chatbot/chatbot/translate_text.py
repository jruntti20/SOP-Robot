from googletrans import Translator
translator = Translator()

class translate_to_english:
    def translate(text, source_language='fi', target_language='en'):
        translated_text = translator.translate(text, src=source_language, dest=target_language).text
        return translated_text



