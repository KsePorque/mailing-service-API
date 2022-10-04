from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mailing_app.models import Client, Message, Mailing
from mailing_app.serializers import ClientSerializer

class ClientAPITestCase(APITestCase):
    def test_get_client_list(self):
        client1 = Client.objects.create(phone_number="7123456789", phone_code=7, tag="new")
        client2 = Client.objects.create(phone_number="7987654321", phone_code=7, tag="new")
        client3 = Client.objects.create(phone_number="7000000000", phone_code=998, tag="old")

        url = reverse('client-list')
        response = self.client.get(url)
        serializer_data = ClientSerializer([client1, client2, client3], many=True).data

        #tests
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertEqual(serializer_data, response.data)


    def test_post_client(self):
        client_data = {
            "phone_number": "70009998704",
            "phone_code": 7,
            "tag": "test"
        }

        url = reverse('client-list')
        response = self.client.post(url, client_data, format='json')
        print(response)

        # tests
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().phone_number, '70009998704')