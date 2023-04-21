from googletrans import Translator

translator = Translator()

def translate(text, src, dest):
    result = translator.translate(text, src=src, dest=dest)
    return result.text.capitalize()