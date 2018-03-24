from django.db import models

class SignUp(models.Model):
    signup_name  = models.CharField(max_length=100)
    signup_email = models.CharField(max_length=100)

    def __unicode__(self):
        return self.signup_name

class ExtraMessage(models.Model):
    msg_date = models.DateField('msg date', blank=False)
    msg_txt = models.CharField('msg text', max_length=2000)

    def __unicode__(self):
	return self.msg_txt.encode('ascii', 'ignore')
