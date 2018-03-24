from django.db import models

class Configuration(models.Model):
    config_param = models.CharField(max_length=75)
    config_value = models.CharField(max_length=200, blank=True)
    config_desc = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{0}={1}".format(self.config_param, self.config_value)

