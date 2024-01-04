from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_on_break = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username + ' -> ' + self.message + ' | ' + str(self.time) + ' | ' + str(self.date)


class Performance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    login_time = models.TimeField(null=True, blank=True)
    work_time = models.IntegerField(null=True, blank=True, default=0)
    break_time = models.IntegerField(null=True, blank=True, default=0)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    break_start_time = models.TimeField(null=True, blank=True)
    break_end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | Date: {self.date} - WT: {self.work_time} - BT: {self.break_time}"