# coding=utf-8
from django.contrib import admin
from pererabotka.models import pererabotka, start, brigada


# Register your models here.
class perAdmin(admin.StackedInline):
    model = pererabotka
    extra = 1

@admin.register(brigada)
class brigAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    inlines = [perAdmin]

@admin.register(start)
class startAdmin(admin.ModelAdmin):
    fields = ['start_text', 'start_description']
    list_display = ['start_text', 'start_description']