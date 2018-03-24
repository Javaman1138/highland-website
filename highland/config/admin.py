from django.contrib import admin
from django import forms
from .models import Configuration

class ConfigurationAdmin(admin.ModelAdmin):

    list_display = ('config_param', 'config_value', 'config_desc')
    list_filter = ('config_param',)
    ordering = ('-config_param',)

admin.site.register(Configuration, ConfigurationAdmin)

