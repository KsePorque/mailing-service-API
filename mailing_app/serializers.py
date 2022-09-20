from django.db.models import Count
from rest_framework import serializers
from mailing_app.models import Client, Mailing, Message


# create logger (is configured in SETTINGS)
import logging
logger = logging.getLogger(__name__)

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MailingSerializer(serializers.ModelSerializer):
    messages_stats = serializers.SerializerMethodField()

    def get_messages_stats(self, instance):
        mailing_pk = instance.pk
        stats_dict = {
            0: 0,
            1: 0,
            2: 0
        }

        stats = Message.objects.filter(from_mailing=mailing_pk).values('status').order_by('status').annotate(total=Count('status'))
        for s in stats:
            #logger.info(f'Statistic data for mailing is {s}')
            #logger.info(f'Status is {s["status"]}')
            #logger.info(f'Number is {s["total"]}')
            stats_dict[s["status"]] = s["total"]

        return stats_dict

    class Meta:
        model = Mailing
        fields = ['id','started_at', 'ended_at', 'text', 'filter_tag', 'filter_code'] # "__all__"
        fields += ['messages_stats']
        readonly = ['messages_stats', 'id']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
