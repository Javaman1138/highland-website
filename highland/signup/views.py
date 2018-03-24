from django.views import generic
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from common import constants
from .models import SignUp
from .forms import SignUpForm
import json
import urllib, urllib2, base64

ALREADY_SIGNED_UP = 'You are already signed up'
SIGNUP_ERROR = 'Unable to sign up, please try again later'

class SignUpView(generic.TemplateView):
    template_name = 'signup.html'
    form_class = SignUpForm

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

                signup_data = self.save_signup(email, name)
            except Exception, e:
                context['error'] = SIGNUP_ERROR

            if not signup_data:
                context['error'] = ALREADY_SIGNED_UP
            else:
                context['success'] = True
                context['email_addr'] = email
                context['person_name'] = name
                context['person_id'] = signup_data.id

                try: 
                    self.send_confirmation(email, Context(context))
                except Exception ,e :
                    context['error'] = str(e) 
	else:	        
            context['errors'] = form.errors

    	return HttpResponse(json.dumps(context), content_type="application/json")

    def save_signup(self, email, name):
        if SignUp.objects.filter(signup_email=email):
            return None
        else:
            signup_obj = SignUp(signup_name=name, signup_email=email)
            signup_obj.save()
            return signup_obj


    def send_confirmation(self, email_addr, context):
        template = 'confirmation-email'
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

class SignUpRemove(generic.TemplateView):
    template_name = 'remove.html'

    def get(self, request, *args, **kwargs):
	email = request.GET.get('email')
	id = request.GET.get('id')
	if (not email) or (not id):
	    raise Http404("WTF")

        context = {
            'success' : False,
            'email' : email,
        }
	try:
	    rows = SignUp.objects.filter(signup_email=email).filter(pk=id)
            if rows:
	        rows.delete()
                context['success'] = True
	except:
	    raise Http404("WTF")

	return render(request, self.template_name, Context(context))

