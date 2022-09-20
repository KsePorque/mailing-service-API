from django.utils.timezone import make_aware
from django.conf import settings
#from django.db.models import Q
from mailing_app.models import Client, Message, Mailing

import asyncio
from datetime import datetime, timedelta

import requests

# async def hello_world():
#     curr_time = datetime.today()
#     end_time = curr_time + timedelta(seconds=5.0)
#     while True:
#         curr_time = datetime.today()
#         if (curr_time + timedelta(seconds=1.0)) >= end_time:
#             break
#
#         print(f"Hello World! Time is {curr_time.time()}")
#         print(f"End time is {end_time.time()}")
#         await asyncio.sleep(1.0)


def send_message_for_mailing(message):
    """Connect to API for email-sending.
    Send message. If successful mark messages as sent"""

    message_id = message.pk
    message_phone = message.to_client.phone_number
    message_text = message.from_mailing.text

    auth_token = settings.FBRQ_TOKEN
    headers = {
        'Authorization': ('Bearer ' + auth_token)
    }
    data = {
        "id": message_id,
        "phone": message_phone,
        "text": message_text
    }

    url_api = f'https://probe.fbrq.cloud/v1/send/{message_id}'
    response = requests.post(url_api, json=data, headers=headers)

    if response.status_code == 200:
        message.status = 1
        message.save()
    elif response.status_code == 400:
        message.status = 0
        message.save()

    print(f'Response status code: {response.status_code}')
    print(f'Response: {response.json()}')



def check_for_pending_messages():
    curr_time = make_aware(datetime.today())

    # Disable sending messages if mailing end time is reached (change status to 0 - not sent)
    not_sent_messages_disabled = Message.objects.filter(status=2).filter(from_mailing__ended_at__lte=curr_time).distinct().select_related()
    for m in not_sent_messages_disabled:
        m.status = 0
    Message.objects.bulk_update(list(not_sent_messages_disabled), ['status'])

    # Only send messages if mailing is started and task is pending
    pending_messages = Message.objects.filter(status=2).filter(from_mailing__started_at__lte=curr_time)

    print(f"Pending messages: {pending_messages}")

    for message in pending_messages:
        send_message_for_mailing(message)

    #asyncio.run(hello_world())
