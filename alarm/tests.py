from django.test import TestCase
from alarm.models import Alarm
from account.models import Beamy

beamy = Beamy(name="Test", version="1.0", pin=4322253)
class Alarm_Param(TestCase):

    def test_default(self):
        alarm_default = Alarm() # Default alarm
        self.assertEqual(alarm_default.is_valid(), True)

    def test_days_format(self):
        alarm_days = Alarm(day="lundi")
        self.assertEqual(alarm_days.is_valid(), False)

    def test_name(self):
        alarm_wrong_name = Alarm(name = 432890, beamy = beamy)
        self.assertEqual(alarm_wrong_name.is_valid(), True)

    def test_enabled_status(self):
        alarm_wrong_status = Alarm(enabled = 'feraok', beamy = beamy)
        alarm_false_status = Alarm(enabled = "false", beamy = beamy)
        alarm_true_status = Alarm(enabled = "true", beamy = beamy)
        self.assertEqual((alarm_wrong_status.is_valid(), alarm_false_status.is_valid(), alarm_true_status.is_valid()), (False, True, True))

    def test_running_status(self):
        alarm_wrong_running_status = Alarm(running = "feroj", beamy = beamy)
        alarm_false_running_status = Alarm(running = "false", beamy = beamy)
        alarm_true_running_status = Alarm(running = "true", beamy = beamy)
        self.assertEqual((alarm_wrong_running_status.is_valid(), alarm_false_running_status.is_valid(), alarm_true_running_status.is_valid()), (False, True, True))

    def test_hour(self):
        alarm_wrong_hour = Alarm(hour = 25, beamy = beamy)
        self.assertEqual(alarm_wrong_hour.is_valid(), False)

    def test_minute(self):
        alarm_wrong_minutes = Alarm(minute = 61, beamy = beamy)
        self.assertEqual(alarm_wrong_minutes.is_valid(), False)