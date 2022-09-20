from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView

from mailing_app.models import Client, Message, Mailing
from mailing_app.serializers import ClientSerializer, MailingSerializer, MessageSerializer


# create logger (is configured in SETTINGS)
import logging
logger = logging.getLogger(__name__)

# Views for client API
class ClientData(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientDataDetail(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# Views for mailing API
class MailingData(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        mailing_data = request.data
        serializer = MailingSerializer(data=mailing_data)
        serializer.is_valid(raise_exception=True)
        current_mailing = serializer.save()
        logger.info(f'Current mailing text is "{current_mailing.text}"')

        try:
            tag_to_filter = serializer.validated_data['filter_tag'] or None
        except:
            tag_to_filter = None

        try:
            code_to_filter = serializer.validated_data['filter_code']
        except:
            code_to_filter = None

        # Filter clients that will receive mailing
        clients_for_mailing = Client.objects.all()
        if tag_to_filter:
            clients_for_mailing = clients_for_mailing.filter(tag=tag_to_filter)
        if code_to_filter:
            clients_for_mailing = clients_for_mailing.filter(phone_code=code_to_filter)

        logger.info(f'Clients that are selected for mailing: {clients_for_mailing}')

        # Create messages that should be sent for this mailing (pending state = 2)
        new_messages = []
        for client in clients_for_mailing:
            new_messages.append(Message(to_client=client, from_mailing=current_mailing, status=2))
        Message.objects.bulk_create(new_messages)
        logger.info(f'Number of pending messages generated: {len(new_messages)}')

        return Response(serializer.data)



class MailingDataDetail(RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingDataStats(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request,*args, **kwargs):
        serializer = MailingSerializer(Mailing.objects.all(), many=True)
        return Response(serializer.data)


class MailingDataDetailStats(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk=None, *args, **kwargs):
        id = pk or request.query_params.get('id')
        messages = Message.objects.filter(from_mailing=id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

