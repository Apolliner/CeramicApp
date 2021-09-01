from modeltranslation.translator import translator, TranslationOptions
from CeramicApp.models import Note


class NoteTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Note.
    """
    
    fields = ('header', 'text',)


translator.register(Note, NoteTranslationOptions)