# -*- coding: utf-8 -*-

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin
from CeramicApp.models import Note


class NoteAdmin(MPTTModelAdmin, TranslationAdmin):
    """
    Настройка админки для Note.
    """
    
    list_display = ('name',)

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }

    fieldsets = [
        (None, {
            'fields': [
                'autor',
                'header',
                'startdate',
            ]
        }),
        (u'Лог', {
            'fields': [
                'author',
                'header',
            ],
            'classes': ['collapse']
        })
    ]

#admin.site.register(Note, NoteAdmin)
