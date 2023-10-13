from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ProfileForm
from .models import Logs, Profile
import datetime


# Create your views here.
class IndexView(TemplateView):
    template_name = 'HR_App/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def post(self, request):
        value = request.POST['is_on_break']
        if value == 'break':
            Profile.objects.filter(user=self.request.user).update(
                is_on_break=True,
                break_start_time=datetime.datetime(
                    datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                    datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second
                )
            )
        else:
            Profile.objects.filter(user=self.request.user).update(
                is_on_break=False,
                break_end_time=datetime.datetime(
                    datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                    datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second
                )
            )
            break_duration = self.get_break_duration()
            self.add_break_time(break_duration)
        return redirect('HR_App:index')

    def get_break_duration(self):
        break_start_time = Profile.objects.get(user=self.request.user).break_start_time
        break_end_time = Profile.objects.get(user=self.request.user).break_end_time
        break_start_time = datetime.datetime.strptime(str(break_start_time), '%Y-%m-%d %H:%M:%S')
        break_end_time = datetime.datetime.strptime(str(break_end_time), '%Y-%m-%d %H:%M:%S')
        break_duration = break_end_time - break_start_time
        return break_duration

    def add_break_time(self, time):
        break_time = Profile.objects.get(user=self.request.user).total_break_time
        break_hours = int(break_time.split(':')[0])
        break_minutes = int(break_time.split(':')[1])
        break_seconds = int(break_time.split(':')[2])
        new_time = datetime.timedelta(hours=break_hours, minutes=break_minutes, seconds=break_seconds)
        total_time = new_time + time
        hours, remainder = divmod(total_time.seconds + total_time.days * 24 * 3600, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_time = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        Profile.objects.filter(user=self.request.user).update(total_break_time=total_time)
        print(f"{self.request.user.username} has took a total break time of {total_time}")


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('HR_App:login')
    template_name = 'HR_App/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.on_signup()
        return super().form_valid(form)

    def on_signup(self):
        """
        This function will create a log for the user who just signed up
        :return:
        """
        Logs.objects.create(
            user=self.request.user,
            message='Signed Up'
        )
        Profile.objects.create(
            user=self.request.user,
            login_time=None,
            login_date=None,
            logout_time=None,
            logout_date=None
        )


class LoginView(TemplateView):
    template_name = 'HR_App/login.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            self.on_login()
            return redirect('HR_App:index')
        else:
            return redirect('HR_App:login')

    def on_login(self):
        """
        This function will create a log for the user who just logged in
        :return:
        """
        Logs.objects.create(
            user=self.request.user,
            message='Logged In'
        )
        Profile.objects.filter(user=self.request.user).update(
            is_on_break=False,
            total_break_time='0:0:0',
        )
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        Profile.objects.filter(user=self.request.user).update(
            login_time=datetime.datetime(year, month, day, hour, minute, second),
        )


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'HR_App/logout.html'

    def post(self, request):
        username = request.user.username
        password = request.POST['password']
        if check_password(password, request.user.password):
            self.on_logout()
            print(self.get_session_duration())
            logout(request)
            return redirect('HR_App:login')
        else:
            return redirect('HR_App:logout')

    def on_logout(self):
        """
        This function will create a log for the user who just logged out
        :return:
        """
        if Profile.objects.get(user=self.request.user).is_on_break:
            Profile.objects.filter(user=self.request.user).update(
                is_on_break=False,
                break_end_time=datetime.datetime(
                    datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                    datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second
                )
            )
            break_duration = self.get_break_duration()
            self.add_break_time(break_duration)
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        Profile.objects.filter(user=self.request.user).update(
            logout_time=datetime.datetime(year, month, day, hour, minute, second),
            is_on_break=False
        )
        Logs.objects.create(
            user=self.request.user,
            message=f'Logged Out, Total Duration: {self.get_session_duration()}'
        )
        self.add_worktime(self.get_session_duration())

    def get_session_duration(self):
        login_time = Profile.objects.get(user=self.request.user).login_time
        logout_time = Profile.objects.get(user=self.request.user).logout_time
        total_break_time = Profile.objects.get(user=self.request.user).total_break_time
        login_time = datetime.datetime.strptime(str(login_time), '%Y-%m-%d %H:%M:%S')
        logout_time = datetime.datetime.strptime(str(logout_time), '%Y-%m-%d %H:%M:%S')
        total_break_time = datetime.datetime.strptime(str(total_break_time), '%H:%M:%S')
        total_break_time = datetime.timedelta(
            hours=total_break_time.hour, minutes=total_break_time.minute, seconds=total_break_time.second
        )
        if login_time and logout_time:
            return (logout_time - login_time) - total_break_time

    def get_break_duration(self):
        break_start_time = Profile.objects.get(user=self.request.user).break_start_time
        break_end_time = Profile.objects.get(user=self.request.user).break_end_time
        break_start_time = datetime.datetime.strptime(str(break_start_time), '%Y-%m-%d %H:%M:%S')
        break_end_time = datetime.datetime.strptime(str(break_end_time), '%Y-%m-%d %H:%M:%S')
        break_duration = break_end_time - break_start_time
        return break_duration

    def add_worktime(self, time):
        worktime = Profile.objects.get(user=self.request.user).legit_working_time
        # total_break_time = Profile.objects.get(user=self.request.user).total_break_time

        workhours = int(worktime.split(':')[0])
        workminutes = int(worktime.split(':')[1])
        workseconds = int(worktime.split(':')[2])

        # total_break_time = datetime.datetime.strptime(str(total_break_time), '%H:%M:%S')
        # total_break_time = datetime.timedelta(
        #     hours=total_break_time.hour, minutes=total_break_time.minute, seconds=total_break_time.second
        # )

        new_time = datetime.timedelta(hours=workhours, minutes=workminutes, seconds=workseconds)
        total_time = new_time + time

        hours, remainder = divmod(total_time.seconds + total_time.days * 24 * 3600, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_time = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        Profile.objects.filter(user=self.request.user).update(legit_working_time=total_time)

        print(f"{self.request.user.username} has a total working time of {total_time}")

    def add_break_time(self, time):
        break_time = Profile.objects.get(user=self.request.user).total_break_time
        break_hours = int(break_time.split(':')[0])
        break_minutes = int(break_time.split(':')[1])
        break_seconds = int(break_time.split(':')[2])
        new_time = datetime.timedelta(hours=break_hours, minutes=break_minutes, seconds=break_seconds)
        total_time = new_time + time
        hours, remainder = divmod(total_time.seconds + total_time.days * 24 * 3600, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_time = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        Profile.objects.filter(user=self.request.user).update(total_break_time=total_time)
        print(f"{self.request.user.username} has took a total break time of {total_time}")


class LogsView(LoginRequiredMixin, ListView):
    model = Logs
    template_name = 'HR_App/logs.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return Logs.objects.order_by('-date', '-time')
