from datetime import datetime, timedelta
import requests

from django.utils.timezone import make_aware
from django.conf import settings
from django.db.models import Count
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

    # logging stats data
    stats = Message.objects.all().values('status').order_by('status').annotate(total=Count('status'))
    stats_dict = { 0: 0, 1: 0, 2: 0}
    for s in stats:
        stats_dict[s["status"]] = s["total"]

    logger.info(f"All messages count: {sum(stats_dict.values())}")
    logger.info(f"Number of pending messages (with status = 2): {stats_dict[2]}")
    logger.info(f"Number of sent messages (with status = 1): {stats_dict[1]}")
    logger.info(f"Number of not sent messages (with status = 0): {stats_dict[0]}")

    logger.info(f"Current time is {curr_time}\n")

    pending_messages_lst = list(pending_messages)
    logger.info(f"Messages that will be send now: {pending_messages}")
    if pending_messages:
        logger.info(f'mailing start time {pending_messages[0].from_mailing.started_at}')

    asyncio.run(send_messages_for_mailing(pending_messages_lst))


