from googletrans import Translator

translator = Translator()

def translate_to_en(text, src_lang):
    if src_lang == 'en':
        return text
    return translator.translate(text, src=src_lang, dest='en').text

def translate_from_en(text, dest_lang):
    if dest_lang == 'en':
        return text
    return translator.translate(text, src='en', dest=dest_lang).text
