from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from common import constants
from common import rotation
from config.models import Configuration
from events.models import Event
from sitedocuments.models import Document
from signup.models import SignUp
from signup.models import ExtraMessage
from email.utils import parseaddr
import datetime
import json
import urllib, urllib2, base64

class Command(BaseCommand):
    help = 'Test Calendar'

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

        test_calendar = TestCalendar()
        test_calendar.rotation_days(week_start_date)

class TestCalendar(object):

    def __init__(self):
        self.config = Configuration.objects.order_by('config_param')
        self.ROTATION_ENABLED = self.get_config_value(constants.ROTATION_DAYS_ENABLED_PARAM)
        self.ROTATION_DAYS = self.get_config_value(constants.ROTATION_DAYS_PARAM).split(",")
        self.ROTATION_START_DATE = self.get_config_value(constants.ROTATION_DAYS_START_PARAM)

    def get_config_value(self, find_config_param):
        for config in self.config:
            if config.config_param == find_config_param:
                return config.config_value
        return ""

    def rotation_days(self, range_start=None, days=constants.DEFAULT_RANGE):

        #get events    
        if not range_start:
            range_start = datetime.datetime.now()
	
        range_end = range_start + datetime.timedelta(days=days)

	rotation_start_date = datetime.datetime.strptime(self.ROTATION_START_DATE, '%m/%d/%Y')
	rotation_builder = rotation.Rotation()
	rotation_list = rotation_builder.determine_rotation_days(rotation_start_date, range_start, range_end)

	print rotation_list

	rotation_days = rotation_builder.get_rotation_days()
        print rotation_days


