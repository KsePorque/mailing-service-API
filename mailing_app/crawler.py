from mailing_app.tasks import check_for_pending_messages
import time

while True:
    check_for_pending_messages()
    time.sleep(5)