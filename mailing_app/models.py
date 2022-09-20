from datetime import datetime, timedelta
import pytz  #for timezones
from django.utils.timezone import make_aware
from django.db import models
from django.core.validators import RegexValidator

# Models for mailing lists
class Client(models.Model):
    TIMEZONES = (
        'Canada/Atlantic',
        'Canada/Central',
        'Canada/Eastern',
        'Canada/Mountain',
        'Canada/Pacific',
    )

    phone_regex = RegexValidator(regex=r'7\d{10}$',
                                 message="Phone number format must be: '7XXXXXXXXXX'. Where X is digit from 0 to 9.")

    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=False)
    phone_code = models.IntegerField(default=7)
    tag = models.CharField(max_length=50, blank=True, null=True)
    #time_zone = models.CharField(max_length=100, blank=True, null=True, choices=TIMEZONES)  # 64 min

    def __str__(self):
        return (f'{self.phone_number} - {self.tag}')

class Mailing(models.Model):
    curr_time = datetime.today()
    end_time = make_aware(curr_time + timedelta(seconds=600))

    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(default=end_time)
    text = models.TextField(max_length=500)
    filter_code = models.IntegerField(blank=True, null=True)
    filter_tag = models.CharField(max_length=50, blank=True, null=True)


class Message(models.Model):
    STATUSES = (
        (1, 'is_sent'),
        (0, 'not_sent'),
        (2, 'is_pending'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=0)
    from_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    to_client = models.ForeignKey(Client, on_delete=models.CASCADE)

