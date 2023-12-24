from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_year = models.CharField(default=datetime.now().year, max_length=4)
    profile_month = models.CharField(default=datetime.now().month, max_length=2)
    login_time = models.CharField(null=True, blank=True, max_length=200)
    logout_time = models.CharField(null=True, blank=True, max_length=200)
    break_start_time = models.CharField(null=True, blank=True, max_length=200)
    break_end_time = models.CharField(null=True, blank=True, max_length=200)
    total_break_time = models.CharField(default="0:0:0", max_length=200)
    legit_working_time = models.CharField(default="0:0:0", max_length=200)
    is_on_break = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' ' + self.profile_year + '-' + self.profile_month


class Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username + ' ' + self.message + ' in', self.time, self.date

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username