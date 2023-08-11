from django.db import models


class ActionLog(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class MAVP(models.Model):
    facility_short = models.CharField(max_length=3, primary_key=True)
    facility_long = models.CharField(max_length=255)
