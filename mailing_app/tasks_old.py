from datetime import datetime, timedelta
import requests

from django.utils.timezone import make_aware
from django.conf import settings
#from django.db.models import Q
from mailing_app.models import Client, Message, Mailing

from asgiref.sync import sync_to_async
import asyncio
import aiohttp

# create logger (is configured in SETTINGS)
import logging
logger = logging.getLogger(__name__)

async def post__send_message(session, url, headers, message):
    message_id = sync_to_async(message.pk)
    message_phone = sync_to_async(message.to_client.phone_number)
    message_text = sync_to_async(message.from_mailing.text)

    data = {
        "id": message_id,
        "phone": message_phone,
        "text": message_text
    }

    async with session.post(url.join(message_id), json=data, headers=headers) as response:
        resp_status_code = sync_to_async(response.status_code)
        if resp_status_code == 200:
            message.status = 1
            sync_to_async(message.save())
        elif resp_status_code == 400:
            message.status = 0
            sync_to_async(message.save())

        logger.info(f'Response status code: {response.status_code}')
        logger.info(f'Response: {response.json()}')


async def send_messages_for_mailing(pending_messages):
    """Connect to API for email-sending.
    Send message. If successful, mark messages as sent"""
    actions = []

    auth_token = settings.FBRQ_TOKEN
    headers = {
        'Authorization': ('Bearer ' + auth_token)
    }

    async with aiohttp.ClientSession() as session:
        url_api = 'https://probe.fbrq.cloud/v1/send/'
        for message in pending_messages:
            actions.append(asyncio.ensure_future(post__send_message(session, url_api, headers=headers, message=message)))

        post_res = await asyncio.gather(*actions)



def check_for_pending_messages():
    curr_time = make_aware(datetime.today())

    # Disable sending messages if mailing end time is reached (change status to 0 - not sent)
    not_sent_messages_disabled = Message.objects.filter(status=2).filter(from_mailing__ended_at__lte=curr_time).distinct().select_related()
    for m in not_sent_messages_disabled:
        m.status = 0
    Message.objects.bulk_update(list(not_sent_messages_disabled), ['status'])

    # Only send messages if mailing is started and task is pending
    pending_messages = Message.objects.filter(status=2).filter(from_mailing__started_at__lte=curr_time)

    logger.info(f"Pending messages: {pending_messages}")

    asyncio.run(send_messages_for_mailing(pending_messages))


