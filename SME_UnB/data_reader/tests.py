from django.test import TestCase
from alerts.models import Alert


class AlertsTestCase(TestCase):
    def test_is_creating_alert_on_database(self):
        all_alerts_number = Alert.objects.count()
