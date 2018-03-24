from django.contrib import admin
from django import forms

from .models import SignUp
from .models import ExtraMessage

class SignUpAdmin(admin.ModelAdmin):
    list_display = ('signup_email', 'signup_name')
    ordering = ('signup_email',)

class ExtraMessageAdmin(admin.ModelAdmin):
    list_display = ('msg_date', 'msg_txt')
    ordering = ('-msg_date',)
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ExtraMessageAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'msg_txt':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

admin.site.register(SignUp, SignUpAdmin)
admin.site.register(ExtraMessage, ExtraMessageAdmin)
