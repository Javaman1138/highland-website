from events.models import Event
from config.models import Configuration
import constants
import datetime
import time


class Rotation(object):

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

    def test_rotation(self):
    	test_date = datetime.datetime(2015, 8, 22)
    	end_date = datetime.datetime(2015, 8, 22)
    	end_date += datetime.timedelta(days=7)
    	for x in range (0, 42):
    	    print self.determine_rotation_days(test_date, end_date)
    	    test_date += datetime.timedelta(days=7)
    	    end_date += datetime.timedelta(days=7)

    def _build_rotation_list(self, rotation_start_date, start_idx, no_school_dates):
        rotation_list = []
        day_range = 5 - rotation_start_date.weekday()
        for cntr in range( 0, day_range):
	    idx = (start_idx) % len(self.ROTATION_DAYS)
            if rotation_start_date.date() in no_school_dates:
            	rotation_list.extend([{'date':rotation_start_date.date(), 'day':'X'}])
            	rotation_start_date += datetime.timedelta(days=1)
            	continue
            else:
            	rotation_list.extend([{'date':rotation_start_date.date(), 'day':self.ROTATION_DAYS[idx]}])
            if rotation_start_date.weekday() > 4:
                break
            else:
                start_idx+=1
	        
	    rotation_start_date += datetime.timedelta(days=1)
	return rotation_list

    def _get_range(self, the_date):
        if the_date.weekday() > 4:
            # start with the following monday
            start_date = the_date
            end_date = start_date + datetime.timedelta(days=6)
        else:
            # start with last monday
            day_of_week = the_date.weekday()
            start_date = the_date - datetime.timedelta(days=day_of_week)
            end_date = the_date + datetime.timedelta(days=6 - day_of_week)

	print "range is {0} - {1}".format(start_date, end_date)
	return (start_date, end_date)

    def email_rotation_days(self, start_date, end_date):
	if not self.ROTATION_ENABLED.lower() in ['true', 'y', 'yes']:
    	    return None
        
	rotation_start = datetime.datetime.strptime(self.ROTATION_START_DATE, '%m/%d/%Y')
	return self.determine_rotation_days(rotation_start, start_date, end_date)
     
    def get_rotation_days(self, delta=0):
	if not self.ROTATION_ENABLED.lower() in ['true', 'y', 'yes']:
    	    return None

        rotation_start = datetime.datetime.strptime(self.ROTATION_START_DATE, '%m/%d/%Y')
    	todays_date = datetime.datetime.now() + datetime.timedelta(days=delta)
        rotation_days = []

        #if rotation day starts this week, we have a special case
	day_of_week = todays_date.weekday() + 1
        if day_of_week == 7:
            day_of_week = 0
        start_of_week = todays_date - datetime.timedelta(days=day_of_week)
        end_of_week = start_of_week + datetime.timedelta(5)

	if start_of_week.date() <= rotation_start.date() <= end_of_week.date(): 
	#if rotation_start > todays_date:
            delta_days = rotation_start.date() - todays_date.date()
            if delta_days.days >= 7:
		# We are not in a school week yet
 	        return None
	    else:
                rotation_days.extend(
			self._prefill_empty_days(rotation_start.date()))
	elif todays_date.date() < rotation_start.date():
	    return None

    	(start_date, end_date) = self._get_range(todays_date)
    	rotation_days.extend(self.determine_rotation_days(rotation_start, start_date, end_date))

        return rotation_days

    def _prefill_empty_days(self, rotation_start):
        """If the start of the school year isn't a monday, we need to prefill
           the rotation days for that given week
	"""
	rotation_days = []
	for x in range(1, rotation_start.weekday()+1):
	    insert_date = rotation_start - datetime.timedelta(days=x)
	    rotation_days.insert(0, {'date': insert_date, 'day': 'X'})
	return rotation_days	

    def determine_rotation_days(self, rotation_start_date, start_date, end_date):

	if rotation_start_date > start_date and rotation_start_date < end_date:
		return self._build_rotation_list(rotation_start_date, 0, [])	

	#get list of 'no school' events up until this weeks range end        
        events = Event.objects.filter(start_date__gte= rotation_start_date).filter(start_date__lte= end_date).filter(event_type=constants.SCHOOL_CALENDAR_TYPE).filter(event_title='No School').order_by('start_date')
        no_school_dates = []
        for event in events:
            if event.end_date:
                total_days = (event.end_date - event.start_date).days + 1
        	for single_date in (event.start_date + datetime.timedelta(x) for x in range(total_days)):
        	    no_school_dates.extend([single_date])
            else:
        	no_school_dates.extend([event.start_date])

	#adjust start date to monday
	if start_date.weekday() > 0:
	    start_date += datetime.timedelta(7 - start_date.weekday())

        day_count = (start_date - rotation_start_date).days + 1
        rotation_count = 0
        
        # check for no school this week
        adjust_day_count = 0
        if start_date.date() in no_school_dates:
	    for single_date in (start_date + datetime.timedelta(n) for n in range (0, 5)):
	        if single_date.date() in no_school_dates:
	            adjust_day_count+=1
		else:
		    break;
	    day_count += adjust_day_count
		
	# No rotation days this week
	if adjust_day_count == 5:
	    return []

	#count the roatation days (weekdays, exclude no school days)
        for single_date in (rotation_start_date + datetime.timedelta(n) for n in range(day_count)):
            if single_date.weekday() in [0,1,2,3,4] and single_date.date() not in no_school_dates:
                rotation_count +=1
        		
	first_rotation_day_this_week = start_date + datetime.timedelta(adjust_day_count)

	#calculate where we are now
        idx = (rotation_count-1) % len(self.ROTATION_DAYS)
	return self._build_rotation_list(start_date, idx, no_school_dates)

