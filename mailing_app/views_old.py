from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from mailing_app.models import Client, Message, Mailing
from mailing_app.serializers import ClientSerializer, MailingSerializer, MessageSerializer

# Views for client API
class ClientData(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ClientSerializer

    def get_queryset(self, *args, **kwargs):
        clients_q = Client.objects.all()
        return clients_q

    def get(self, request, *args, **kwargs):
        serializer = ClientSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        client_data = request.data
        serializer = ClientSerializer(data=client_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ClientDataDetail(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ClientSerializer

    def get_queryset(self, *args, **kwargs):
        clients_q = Client.objects.all()
        return clients_q

    def get_object(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def get(self, request, pk=None, *args, **kwargs):
        id = pk or request.query_params.get('id')
        serializer = ClientSerializer(self.get_object(id))
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views for mailing API
class MailingData(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = MailingSerializer

    def get_queryset(self, *args, **kwargs):
        mailing_q = Mailing.objects.all()
        return mailing_q

    def get(self, request, *args, **kwargs):
        serializer = MailingSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        mailing_data = request.data
        serializer = MailingSerializer(data=mailing_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MailingDataDetail(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = MailingSerializer

    def get_queryset(self, *args, **kwargs):
        mailing_q = Mailing.objects.all()
        return mailing_q

    def get_object(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def get(self, request, pk=None, *args, **kwargs):
        id = pk or request.query_params.get('id')
        serializer = MailingSerializer(self.get_object(id))
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        mailing = self.get_object(pk)
        serializer = MailingSerializer(mailing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mailing = self.get_object(pk)
        mailing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MailingDataStats(APIView):
    authentication_classes = []
    permission_classes = []

    #def get_queryset(self, *args, **kwargs):
    #    mailing_q = Mailing.objects.all()
    #    return mailing_q

    def get_object(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def get(self, request,*args, **kwargs):
        serializer = MailingSerializer(Mailing.objects.all(), many=True)
        return Response(serializer.data)

class MailingDataDetailStats(APIView):
    authentication_classes = []
    permission_classes = []

    #def get_queryset(self, *args, **kwargs):
    #    mailing_q = Mailing.objects.all()
    #    return mailing_q

    def get_object(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def get(self, request, pk=None, *args, **kwargs):
        id = pk or request.query_params.get('id')
        messages = Message.objects.filter(from_mailing=id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

