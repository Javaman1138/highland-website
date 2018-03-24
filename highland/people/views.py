
from django.views import generic
from .models import ExecutiveMember, CommitteeMember
from .models import Committee
from .forms import CommitteeSignUpForm
from django.shortcuts import render
from common import constants
from django.http import HttpResponse
import json
import urllib, urllib2, base64

ALREADY_SIGNED_UP = 'You are already signed up'
SIGNUP_ERROR = 'Unable to sign up, please try again later'

class ExecutiveView(generic.ListView):
    template_name = 'executives.html'

    def get(self, request):
        executive_list = []
        show_photo=False
        try:
    	    if request.GET.get('photo'):
                show_photo=True
        except:
            show_photo=False

    	for idx, executive in enumerate(ExecutiveMember.objects.all().order_by('position')):
    	    if executive.person_email:
    	        email = executive.person_email.split('@')
    	    else:
    	        email = [None, None]

    	    executive_list.append(
    	    {'position': executive.position,
    	     'idx': idx,
    	     'name': executive.person_name,
    	     'photo': executive.person_photo,
    	     'email1': email[0],
    	     'email2': email[1]
    	    })
    	context = {
    	    'executive_list':executive_list,
	    'show_photo':show_photo,
    	}

    	return render(request, self.template_name, context)

class CommitteeView(generic.ListView):
    template_name = 'chairs.html'

    def get(self, request):
        committees = Committee.objects.all().order_by('committee_title')
	committee_chairs = []
	
    	for idx, chair in enumerate(CommitteeMember.objects.all().select_related('committee')):
    	    if chair.person_email:
    	        email = chair.person_email.split('@')
    	    else:
    	        email = [None, None]
    	    committee_chairs.append(
    	    {'committee': chair.committee.committee_title,
    	     'idx': idx,
    	     'name': chair.person_name,
    	     'email1': email[0],
    	     'email2': email[1]
    	    })
	sorted_list = sorted(committee_chairs, key=lambda k: k['committee'])
    	context = {
	    'committee_chairs' : sorted_list,
    	    'committee_list':committees
    	}

    	return render(request, self.template_name, context)

class CommitteeChairView(generic.ListView):
    template_name = 'chairs.html'

    def get(self, request):
        committees = Committee.objects.all().order_by('committee_title')
	committee_chairs = []
	
    	for idx, chair in enumerate(CommitteeMember.objects.all().select_related('committee')):
    	    if chair.person_email:
    	        email = chair.person_email.split('@')
    	    else:
    	        email = [None, None]

    	    committee_chairs.append(
    	    {'committee': chair.committee.committee_title,
    	     'idx': idx,
    	     'name': chair.person_name,
    	     'email1': email[0],
    	     'email2': email[1]
    	    })
	sorted_list = sorted(committee_chairs, key=lambda k: k['committee'])
    	context = {
	    'committee_chairs' : sorted_list,
    	    'committee_list':committees
    	}

    	return render(request, self.template_name, context)

class CommitteeSignUpView(generic.TemplateView):
    template_name = 'committee-signup.html'
    form_class = CommitteeSignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
	    'form': form,
	    'prompt': True,
	}
	return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        context = {
                   'success': False,
                   'our_addr': constants.OUR_EMAIL
                  }

        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email'].lower()
                committee = form.cleaned_data['committee']

                signup_data = self.save_committee_signup(email, name, committee)
            	if not signup_data:
                	context['error'] = ALREADY_SIGNED_UP
            except Exception, e:
		signup_data = None
                context['error'] = SIGNUP_ERROR
            
	    if signup_data:
                context['success'] = True
                context['email_addr'] = email
                context['person_name'] = name
                context['person_id'] = signup_data.id
		context['committee_id'] = signup_data.committee.id
		context['committee_name'] = signup_data.committee.committee_title
                try: 
                    self.send_confirmation(email, Context(context))
                except Exception ,e :
                    context['error'] = str(e) 
	else:	        
            context['errors'] = form.errors

    	return HttpResponse(json.dumps(context), content_type="application/json")

    def save_committee_signup(self, email, name, committee_id):
        if CommitteeMember.objects.filter(person_email=email,
				          committee=committee_id):
            return None
        else:
            committee_obj = CommitteeMember(person_name=name,
					    person_email=email,
					    committee=committee_id)
            committee_obj.save()
            return committee_obj


    def send_confirmation(self, email_addr, context):
        template = 'committee-confirmation-email'
    	plaintext = get_template(template + ".txt")
	htmly = get_template(template + '.html')
        text_content = plaintext.render(context)
        html_content = htmly.render(context)

        base64string = base64.encodestring('api:%s' % constants.API_KEY).replace('\n', '')
        headers={"Authorization" : "Basic %s" % base64string}
	data = urllib.urlencode(
	        {"from": constants.OUR_EMAIL,
                 "to": email_addr, 
                 "subject": constants.CONFIRMATION_SUBJECT,
                 "text": text_content,
                 "html": html_content})
        request = urllib2.Request(constants.POST_URL, data, headers=headers)
        response = urllib2.urlopen(request).read()

