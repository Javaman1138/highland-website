from django.views import generic
from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import DocumentType, Document

class DocumentView(generic.TemplateView):

    template_name = 'documents.html'

    def get(self, request, *args, **kwargs):

        doc_type = kwargs['doc_type'] if kwargs.has_key('doc_type') else None
        order_by = '-docdate'
	if kwargs.has_key('order') and kwargs['order'] == 'alpha':
	    order_by = 'docname'

    	if doc_type:
            documents = Document.objects.filter(doctype=doc_type).order_by(order_by)
        else:
            documents = Document.objects.all().order_by(order_by)
        context = {'documents': documents}
        return render(request, self.template_name, context)

class LatestDocumentView(generic.TemplateView):

    template_name = 'document.html'

    def get(self, request, *args, **kwargs):

	doc_type = kwargs['doc_type']
	
	try:
            document = Document.objects.filter(doctype=doc_type).latest('docdate')
        except:
            document = None
        
        context = {'document': document}
        return render(request, self.template_name, context)
