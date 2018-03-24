from django.db import models

class EventType(models.Model):
    event_type_desc = models.CharField(max_length=50)

    def __unicode__(self):
        return self.event_type_desc

class Event(models.Model):
    event_title = models.CharField(max_length=75)
    event_desc  = models.CharField(max_length=200, blank=True)
    start_date  = models.DateField('event start date', blank=False)
    start_time  = models.TimeField('event start time', blank=True, null=True)
    end_date    = models.DateField('event end date', blank=True, null=True)
    end_time    = models.TimeField('event end time', blank=True, null=True)
    event_type  = models.ForeignKey(EventType)

    def __unicode__(self):
        return self.event_title

class NewsItem(models.Model):
    news_title = models.CharField(max_length=75)
    news_long  = models.CharField(max_length=4000)
    news_image = models.FileField(upload_to='documents/news_image')
    news_date  = models.DateField('news date', blank=False)
    added_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.news_title

