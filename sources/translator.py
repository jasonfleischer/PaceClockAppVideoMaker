from googletrans import Translator
from sources.log import Log
import os
import json

class Translations:
    def __init__(self, language_code):
        self.language_code = language_code
        self.translations_list = []

translation_file_path = "resources/translation_data.json"
current_langage_code = ""
language_codes = ["en", "de", "es", "fr", "it", "ja", "ko", "pt"]
translation_keys = []

def set_current_langage_code(code):
    global current_langage_code
    current_langage_code = code

def TR(translation_key):
    global current_langage_code
    if current_langage_code == "en":
        translation_keys.append(translation_key)
        return translation_key
    else:
        with open(translation_file_path, 'r') as json_file:
            data = json.load(json_file)
            return data[current_langage_code][translation_key]

def do_translations():
    if os.path.exists(translation_file_path):
        return
    all_translations = []
    for language_code in language_codes:
        translations = Translations(language_code)
        for key in translation_keys:
            translations.translations_list.append((key, translate_text(key, language_code)))
        all_translations.append(translations)

    with open(file_path, 'w') as json_file:
        json.dump(all_translations, json_file, indent=4)

def translate_text(text, target_language):
    if target_language == "en":
        return text
    # TODO: not working anymore
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest=target_language)
    return translated_text.text