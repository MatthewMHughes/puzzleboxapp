import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Dial(models.Model):
    dialPosition = models.IntegerField(default=0)
    dialNumber = models.IntegerField(default=0)
    pistonPosition = models.IntegerField(default=0)
    dialLetter = models.CharField(max_length=1, default="A")
    dialCenter = models.CharField(max_length=1, default="A")
    firstLink = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="first_linked_dial")
    firstLinkDir = models.IntegerField(default=1)
    secondLink = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="second_linked_dial")
    secondLinkDir = models.IntegerField(default=1)
    def __str__(self):
        return str(self.dialNumber)