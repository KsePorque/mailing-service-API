from django.db.models import Count
from rest_framework import serializers
from mailing_app.models import Client, Mailing, Message

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        #readonly = ["modified_at", "created_at"]


class MailingSerializer(serializers.ModelSerializer):
    messages_stats = serializers.SerializerMethodField()

    def get_messages_stats(self, instance):
        mailing_pk = instance.pk
        stats = Message.objects.filter(from_mailing=mailing_pk).values('status').order_by('status').annotate(total=Count('status'))
        return stats #instance.business_account.feedbackmodel_set.aggregate(average_rating=('rating'))['average_rating']

    class Meta:
        model = Mailing
        fields = ['id','started_at', 'ended_at', 'text', 'filter_tag', 'filter_code'] # "__all__"
        fields += ['messages_stats']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
