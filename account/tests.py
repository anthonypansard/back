from django.test import TestCase
from account.models import Device

class DeviceName(TestCase):
    def test_device_name_1(self):
        """
        Makes sure Deviceuser doesn't accept non str arguments for name
        """
        Device_User_1 = Device(name = 8732, imei = 134452)
        self.assertEqual(Device_User_1.is_valid(), False)

    def test_device_name_2(self):
        """
        Makes sure Device doesn't accept a float for imei
        """
        Device_User = Device(imei = "123")
        self.assertEqual(Device_User.is_valid(), False)
