from django.contrib import admin
from mailing_app.models import Client, Message, Mailing

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Mailing)