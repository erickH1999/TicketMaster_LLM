from django.db import models


# Create your models here.

# model to hold saved events attributes -NT
class Events(models.Model):
    event_name = models.CharField(max_length=100, blank=True, null=True)
    event_hall_name = models.CharField(max_length=100, blank=True, null=True)
    event_address = models.CharField(max_length=100, blank=True, null=True)
    event_city = models.CharField(max_length=100, blank=True, null=True)
    event_state = models.CharField(max_length=100, blank=True, null=True)
    event_date = models.CharField(max_length=100, blank=True, null=True)
    event_time = models.CharField(max_length=100, blank=True, null=True)
    event_img = models.URLField(max_length=200, blank=True, null=True)
    event_ticket_link = models.CharField(max_length=100, blank=True, null=True)
    event_favorite = models.BooleanField(default=False)
