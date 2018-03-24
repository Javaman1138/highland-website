from django.db import models
from datetime import datetime

class DocumentType(models.Model):
    doctype = models.CharField(max_length=50)

    def __str__(self):
        return self.doctype

class Document(models.Model):
    docname = models.CharField(max_length=150)
    doctype = models.ForeignKey(DocumentType)
    docdate = models.DateField(blank=False, default=datetime.now)
    docfile = models.FileField(upload_to='documents/uploads')

    def __str__(self):
        return self.docname
