from django.contrib import admin
from .models import DocumentType, Document

def send_published_alert(modeladmin, request, queryset):
    print 'Not Yet Implemented'

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('docname', 'doctype', 'docdate')
    list_filter = ('doctype',)
    ordering = ('-id',)
    actions = [send_published_alert]

admin.site.register(DocumentType)
admin.site.register(Document, DocumentAdmin)

