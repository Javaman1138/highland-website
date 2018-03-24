from django.http import HttpResponse
from django.views import generic
from events.views import EventView, NewsView
from signup.views import SignUpView
from people.views import ExecutiveView, CommitteeChairView
from sitedocuments.views import DocumentView, LatestDocumentView

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        event_view = EventView()
	news_view = NewsView()
	signup_view = SignUpView()
        context = { 
        	'upcoming_events_view': event_view.get(request).content,
        	'news_items_view': news_view.get(request).content,
        	'signup_view': signup_view.get(request).content,
        }
        return self.render_to_response(context)

class CalendarView(generic.TemplateView):
    template_name = 'calendar.html'

    def get(self, request, *args, **kwargs):
        context = { }
        return self.render_to_response(context)


class GenericView(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        context = {}
        return self.render_to_response(context)

class SignUpLandingView(generic.TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        signup_view = SignUpView()
        context = {
                'signup_view': signup_view.get(request).content,
        }
        return self.render_to_response(context)

class ContactView(generic.TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
    	exec_view = ExecutiveView()
        signup_view = SignUpView()
        context = {
                'signup_view': signup_view.get(request).content,
        	'exec_view': exec_view.get(request).content,
        }
        return self.render_to_response(context)

class MeetingView(generic.TemplateView):
    template_name = 'meetings.html'

    def get(self, request, *args, **kwargs):
    	document_view = DocumentView()
    	latest_view = LatestDocumentView()
        context = { 
        	'newsletter_archive_view': document_view.get(request, **{'doc_type':1}).content,
        	'meeting_minutes_view': document_view.get(request, **{'doc_type':2}).content,
        	'latest_newsletter_view': latest_view.get(request, **{'doc_type':1}).content,
        	'forms_view': document_view.get(request, **{'doc_type':3,'order':'alpha'}).content,
        }
        return self.render_to_response(context)

class VolunteerView(generic.TemplateView):
    template_name = 'volunteer.html'

    def get(self, request, *args, **kwargs):
    	committee_view = CommitteeChairView()
        context = { 
        	'committee_view': committee_view.get(request).content,
        }
        return self.render_to_response(context)
