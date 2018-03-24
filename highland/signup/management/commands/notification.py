from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from common import constants
from common import rotation
from events.models import Event
from sitedocuments.models import Document
from signup.models import SignUp
from signup.models import ExtraMessage
from email.utils import parseaddr
import datetime
import json
import urllib, urllib2, base64

class Command(BaseCommand):
    help = 'Send email notification'

    def add_arguments(self, parser):
        pass

    def try_parsing_date(self, text):
        for fmt in ('%m-%d-%Y', '%m/%d/%Y', '%Y%m%d'):
            try:
                return datetime.datetime.strptime(text, fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found')

    def handle(self, *args, **options):
        week_start_date = None
        test_mode_email = None
        for arg in args:
	    try:
                week_start_date = self.try_parsing_date(arg)
	        print 'specified start date: ' + str(week_start_date)
	    except Exception, e:
		test_mode_email = parseaddr(arg)[1]
		print 'test mode, send to: ' + test_mode_email
		pass

        send_notification = SendNotification()
        if test_mode_email:
            send_notification.set_test_mode(test_mode_email)
        send_notification.send_event_notifications(week_start_date)

class SendNotification(object):

    test_mode_email = None
    def set_test_mode(self, email):
	self.test_mode_email = email

    def send_event_notifications(self, range_start=None, days=constants.DEFAULT_RANGE):

        #get events    
        if not range_start:
            range_start = datetime.datetime.now()
	
        range_end = range_start + datetime.timedelta(days=days)
        print 'ruuning auto notifcation for: ' + str(range_start) + ' - ' + str(range_end)

        events = Event.objects.filter(start_date__gte= range_start).filter(start_date__lte= range_end).order_by('start_date')
        newsletter = Document.objects.filter(docdate__gte= range_start).filter(docdate__lte= range_end).filter(doctype=constants.PTANewsletter_type)
        xtra_message = ExtraMessage.objects.filter(msg_date__gt= range_start).filter(msg_date__lte= range_end)
 
	if (((events is None) or (len(events) == 0)) and ((xtra_message is None) or (len(xtra_message) == 0))):
	    print 'Nothing to send out this week.  Aborting'
            return

	recipient_vars = {constants.OUR_EMAIL: 
		{'email':constants.OUR_EMAIL, 'name':'myself', 'id':0}}

        if self.test_mode_email:
            recipient_vars[self.test_mode_email] = {'id':0,
                   				    'email':self.test_mode_email,
            					    'name':self.test_mode_email}
        else:	
	    #get subscribers
            subscribers = SignUp.objects.all()
            for subscriber in subscribers:
                recipient_vars[subscriber.signup_email] = {'id':subscriber.id,
             	         				   'email':subscriber.signup_email,
            					           'name':subscriber.signup_name}
	
        print 'sending to ' + str(len(recipient_vars.keys())) + ' email addresses.'
	print 'there are ' + str(len(events)) + ' events.'
	print '      and ' + str(len(newsletter)) + ' newsletters.'
	print '      and ' + str(len(xtra_message)) + ' extra messages.'

	rotation_builder = rotation.Rotation()
	rotation_list = rotation_builder.email_rotation_days(range_start, range_end)
        sent = self._send_email(recipient_vars, Context({'events':events,
							 'newsletter':newsletter,
							 'rotation_list': rotation_list,
							 'extra_msg':xtra_message}), 'notification-email')
	if sent:
	    print 'success!'
	else:
	    print 'fail!'

    def _send_email(self, recipients, context, template, attachment=None):
    	plaintext = get_template(template + ".txt")
	htmly = get_template(template + '.html')
        text_content = plaintext.render(context)
        html_content = htmly.render(context)

        attachments = []
	if attachment:
	    attachments = [("attachment", open(settings.MEDIA_ROOT + attachment.replace('media','')))]
	
    	try:
            base64string = base64.encodestring('api:%s' % constants.API_KEY).replace('\n', '')
            headers={"Authorization" : "Basic %s" % base64string}
	    data = urllib.urlencode(
	        {"from": constants.OUR_EMAIL,
                 "to": ','.join(recipients.keys()),
                 "subject": constants.REMINDER_SUBJECT,
                 "recipient-variables" : json.dumps(recipients),
                 "text": text_content,
                 "html": html_content})
            request = urllib2.Request(constants.POST_URL, data, headers=headers)
            response = urllib2.urlopen(request).read()
	    print response
	    return True
	except Exception, e:
	    print 'ERROR'
	    print str(e)
	    return False    

