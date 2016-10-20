from __future__ import unicode_literals

from django.db import models
from transductor.models import Transductor, EnergyTransductor
from django.contrib.auth.models import User

class Alert(models.Model):
    status = models.BooleanField()
    description = models.CharField(max_length=50)
    creation_date = models.DateTimeField('date published')
    priority = models.IntegerField()
    transductor = models.ForeignKey(EnergyTransductor)
    user = models.ForeignKey(User)

    def __init__(self, status, description, creation_date, priority, transductor, user):
        self.status = status
        self.description = description
        self.creation_date = creation_date
        self.priority = priority
        self.transductor = transductor
        self.user = user

    def create_alerts(list_user, status, message, collection_time, priority, transductor_id):
        for user in list_user:
            alert = Alert(status, message, collection_time, priority, transductor_id, user.id)
            alert.save()

    class Meta:
        permissions = (
            ("can_check_alerts", "Can Check Alerts"),
        )
