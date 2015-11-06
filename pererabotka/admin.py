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

'''class perAdmin(admin.ModelAdmin):
    fields = ['per_to_brigada', 'p_id', ('p_date_start', 'p_date_finish'), 'p_address', 'p_description', 'p_driver_name', 'hours_cost',
              'den', 'noch','total_hours', 'total_sum']
    list_display = ['per_to_brigada', 'p_id', 'p_date_start', 'p_date_finish', 'p_address', 'p_description', 'p_driver_name', ]
    list_filter = ['p_date_start']'''

@admin.register(start)
class startAdmin(admin.ModelAdmin):
    fields = ['start_text', 'start_description']
    list_display = ['start_text', 'start_description']