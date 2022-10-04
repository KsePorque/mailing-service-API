from django.test import TestCase
from django.conf import settings

from mailing_app.models import Client, Message, Mailing
from mailing_app.serializers import ClientSerializer

class ClientSerializerTestCate(TestCase):
    def test_ok(self):
        client1 = Client.objects.create(phone_number="7123456789", phone_code=7, tag="new", time_zone="Europe/Istanbul")
        client2 = Client.objects.create(phone_number="7987654321", tag="old")
        client3 = Client.objects.create(phone_number="7000000000", phone_code=998)

        serializer_data = ClientSerializer([client1, client2, client3], many=True).data
        expected_data = [
            {
                'id': client1.id,
                'phone_number': "7123456789",
                'phone_code': 7,
                'tag': "new",
                'time_zone': "Europe/Istanbul"
            },
            {
                'id': client2.id,
                'phone_number': "7987654321",
                'phone_code': 7,
                'tag': "old",
                'time_zone': settings.TIME_ZONE
            },
            {
                'id': client3.id,
                'phone_number': "7000000000",
                'phone_code': 998,
                'tag': None,
                'time_zone': settings.TIME_ZONE
            },
        ]

        self.assertEqual(expected_data, serializer_data)