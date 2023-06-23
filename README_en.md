... EN version is in progress ...
# Mailing Service
Mailing service API <br>
Functionality: REST API, Swagger UI, Admin Console (basic), Logging<br>
<b>UPD:</b> docker creation files added (is launched on localhost:8080) 

**Logic**: Every 5 seconds the system checks whether there are messages with status Pending (waiting for email sending). 
- For Pending messages: checking the start and end time of the mailing
- For Pending messages that can be sent now: Send-email task is created
- For non-relevant messages (messages that for some reason haven't been sent): status is changed to not-sent.
- If email-sending service returns 400: message status is changed to not sent (and is not resent)
- If email-sending service returns other error code (service malfunction occurred): task remains in Pending status (may be resent later)



# Tech Stack
Django Rest Framework, SQLite

# Project Details
## Database model
Database Tables:
* Mailing = info about mailing
* Client = info about client
* Message = a message: 
        - has 2 foreign keys connecting with Mailing and Client tables<br>
        - possible statuses: sent, not sent, pending

## Admin Console
Is accessible via /admin/
Admin console may be used to add mailings. <br>

## API Description
API documentation is available by api/v1/docs/ (Swagger UI)
- api/v1/clients  - receive the list of clients and add a new one
- api/v1/clients/<client_id> - get information about the client, modify data, delete client

- api/v1/mailings  - get the list of all mailing lists (includes info about the number of sent messages grouped by message statuses)
- api/v1/mailings/<mailing_id> - get info about the specific mailing, modify/delete mailing list
- api/v1/mailings/<mailing_id>/stats - detailed statistics about messages for a mailing list

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
- Install environmental variable FBRQ_TOKEN (in file .env). This variable contains the authentication token for mail-sending service: https://probe.fbrq.cloud/docs <br>
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






