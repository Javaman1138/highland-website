from django.db import models

class ExecutivePosition(models.Model):
    order_index    = models.IntegerField()
    position_title = models.CharField(max_length=100)
    position_descr = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.position_title
        
class ExecutiveMember(models.Model):
    person_name  = models.CharField(max_length=100)
    person_email = models.CharField(max_length=100, null=True, blank=True)
    position     = models.ForeignKey(ExecutivePosition)
    person_photo = models.FileField(upload_to='photos/executives')

    def __str__(self):
        return self.person_name

class Committee(models.Model):
    committee_title = models.CharField(max_length=100)
    committee_descr = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.committee_title

class CommitteeMember(models.Model):
    person_name  = models.CharField(max_length=100)
    person_email = models.CharField(max_length=100, null=True, blank=True)
    committee    = models.ForeignKey(Committee)
    is_chair     = models.BooleanField()

    def __str__(self):
        return self.person_name

