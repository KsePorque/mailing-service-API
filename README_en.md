# Mailing Service
**Idea**: Mailing is sending specific messages to selected users in specific period of time. For example, you may want to send "Welcome"-message to all the users that are marked with tag New in the database. Or send "You may upgrade for free" message for the old users, but this mailing should start tomorrow and last for 2 days. <br>
This mailing service API is managing all the mailings you have registered to ensure that all messages are sent in time and to proper users<br>
Third-party API is called to send the message: https://probe.fbrq.cloud/docs <br>
<br>
**Functionality**: REST API, Swagger UI, Admin Console (basic), Logging<br>
**UPD**: docker creation files added (is launched on localhost:8080) 

**Logic**: Every 5 seconds the system checks whether there are messages with status Pending (waiting for sending). 
* For Pending messages: the start and end time of the mailing is checked (to know if its time to send them)
* For Pending messages that can be sent now (time is correct): message-sending task is created - request to external API
* For non-relevant messages (messages that for some reason haven't been sent): status is changed to not-sent
* If message-sending service returns 400: message status is changed to not sent (and it would not be resent)
* If message-sending service returns other error code (temporal service malfunction occurred): task remains in Pending status (may be resent later)



# Tech Stack
Django Rest Framework, SQLite

# Project Details
## Database model
Database Tables:  <br> <br>
**Mailing** (info about mailing)<br>
* **id**: unique identifier 
* **start time**: messages should only be sent after this time <br>
* **message**: message that should be sent to clients <br>
* **filter** (tag, phone code): defines clients that should receive the message <br>
* **end time**: no messages should be sent after this time even if not all messages were sent <br>

**Client** (info about client) <br>
* **id**: unique identifier 
* **phone number**: format 7XXXXXXXXXX (X is 0-9) <br>
* **phone code**: the code of the operator <br>
* **tag**: any tag for filtering (for example, new/old/etc) <br>
* **time zone**

**Message** (represents a message to a specific client with a specific text):  <br>
* **id**: unique identifier of the message  <br>
* **creation time**: time when the message was created  <br>
* **status**: possible statuses are sent, not sent, pending  <br>
* **client id** (foreign key): id of the client  <br>
* **mailing id** (foreign key): id of the corresponding mailing   <br>

## Admin Console
Is accessible via _/admin/_ <br>
Admin console may be used to add mailings. <br>

## API Description
API documentation is available by _api/v1/docs/_ (Swagger UI)
- _api/v1/clients_  - receive the list of clients and add a new one
- _api/v1/clients/<client_id>_ - get information about the client, modify data, delete client

- _api/v1/mailings_  - get the list of all mailing lists (includes info about the number of sent messages grouped by message statuses)
- _api/v1/mailings/<mailing_id>_ - get info about the specific mailing, modify/delete mailing list
- _api/v1/mailings/<mailing_id>/stats_ - detailed statistics about messages for a mailing list

## Logging
(in some modules) Logger is created to record information in the logs. Used for debugging <br> 
Currently logger is configured to display info in console

## Testing 
(for clients API only)<br>
Unit tests: APITestCase and django TestCase<br>
To launch: <br>
* API: python manage.py test tests.test_api
* serializers: python manage.py test tests.test_serializers


# Run Project
- Install requirements from requirements.txt: pip install -r requirements.txt
- Apply migrations: python manage.py migrate
- Install environmental variable FBRQ_TOKEN (in file .env). This variable contains the authentication token for message-sending service: https://probe.fbrq.cloud/docs <br>
- Run the server: python manage.py runserver 127.0.0.1:8080
- Start automatic mailing tasks creation (to send emails with message from the mailing) - see steps below <br>

**Or:** <br>
- Start docker: docker build mailing_service

## Automatic tasks creation
As celery is not working on windows, crawler.py may be used to start automatic tasks creation <br>
**Run automatic check for pending tasks:**
 Start crawler: python manage.py runscript crawler
<br><br>
(Also can be launched from shell: <br>
- Open django shell: python manage.py shell
- Run crawler: import mailing_app.crawler)






