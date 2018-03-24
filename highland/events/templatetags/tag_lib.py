
from django import template
from django.template.defaultfilters import stringfilter
import datetime

register = template.Library()

TODAY = 'Today'
TONIGHT = 'Tonight'
YESTERDAY = 'Yesterday'
LAST_NIGHT = 'Last Night'
TOMORROW = 'Tomorrow'
TOMORROW_NIGHT = 'Tomorrow Night'

@register.filter(name='human_date')
@stringfilter
def human_date(string_date, is_night=False):
    """ Humanize the date
        Allow a date to be shown as Today, Yesterday, or Tomorrow
        string_date, is a string date in one of the accepted formats
        is_night, use night references rather than day 

        usage: {{ "6-18-2015"|human_date:"1" }}   - use night notation
        usage: {{ "6-18-2015"|human_date }}       - use day notation (default)
        you can add another filter 'upper' 'lower' to format the text
    """
    format_list = ['%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d']

    today = datetime.date.today()

    #attempt to create date object
    date_value = None
    for format in format_list:
        try:
            date_value = datetime.datetime.strptime(string_date, format).date()
        except:
            pass
  
    #default to string date provided 
    show_date = string_date 

    #convert to word dates if applicable
    if date_value and (date_value == today):
        show_date = TONIGHT if is_night else TODAY
    elif date_value and (today == (date_value + datetime.timedelta(days=1))):
        show_date = LAST_NIGHT if is_night else YESTERDAY
    elif date_value and (today == (date_value - datetime.timedelta(days=1))):
        show_date = TOMORROW_NIGHT if is_night else TOMORROW

    return show_date
