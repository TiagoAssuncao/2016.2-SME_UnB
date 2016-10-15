from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Alert(models.Model):
    status = models.BooleanField()
    description = models.CharField(max_length=50)
    creation_date = models.DateTimeField('date published')
    local = models.CharField(max_length=50)
    priority = models.IntegerField()

    class Meta:
        permissions = (
            ("can_check_alerts", "Can Check Alerts"),
        )

