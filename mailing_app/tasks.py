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
    logger.info("Inside the post__send_message function")

    message_id = message.pk
    logger.info(f"message id: {message_id}")

    message_from_mailing = await sync_to_async(lambda: message.from_mailing)()
    message_text = message_from_mailing.text
    #logger.info(f"message_text: {message_text}")

    message_to_client = await sync_to_async(lambda: message.to_client)()
    message_phone = message_to_client.phone_number
    logger.info(f"message_phone: {message_phone}")

    data = {
        "id": message_id,
        "phone": message_phone,
        "text": message_text
    }

    url_message = url + str(message_id)
    #logger.info(f'url_message {url_message}')
    async with session.post(url_message, json=data, headers=headers) as response:
        resp_status_code = response.status
        if resp_status_code == 200:
            message.status = 1
            await sync_to_async(message.save)()
        elif resp_status_code == 400:
            message.status = 0
            await sync_to_async(message.save)()

        logger.info(f'Response status code: {response.status}')
        #logger.info(f'Response: {response.json()}')


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
        #logger.info(f'url_api: {url_api}')
        for message in pending_messages:
            #logger.info(f'Message: {message}')

            task = asyncio.create_task(post__send_message(session, url_api, headers=headers, message=message))
            # task = asyncio.ensure_future(post__send_message(session, url_api, headers=headers, message=message))
            actions.append(task)

        return await asyncio.gather(*actions)



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

    pending_messages_lst = list(pending_messages)
    asyncio.run(send_messages_for_mailing(pending_messages_lst))


