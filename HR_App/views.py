from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ProfileForm
from .models import Logs, Profile, User, Performance
import datetime
from django.contrib import messages


def create_log(user, message):
    Logs.objects.create(
        user=user,
        time=datetime.datetime.now(),
        message=message
    )


# Create your views here.
class IndexView(TemplateView):
    template_name = 'HR_App/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def post(self, request):
        value = request.POST['is_on_break']
        profile = Profile.objects.filter(user=self.request.user)
        performance = Performance.objects.filter(user=self.request.user)
        now = datetime.datetime.now()
        if value == 'break':
            profile.update(is_on_break=True)
            performance.update(break_start_time=now.time())
            create_log(self.request.user, 'Started Break')
            messages.success(request, 'Break Started')
        else:
            profile.update(is_on_break=False)
            performance.update(break_end_time=now.time())
            performance_obj = performance.get(date=now.date())
            start_time = performance_obj.break_start_time
            end_time = performance_obj.break_end_time
            break_time = ((end_time.hour * 3600) + (end_time.minute * 60) + end_time.second) - (
                        (start_time.hour * 3600) + (start_time.minute * 60) + start_time.second)

            # Update Performance break time
            performance_obj.break_time += break_time
            performance_obj.save()
            create_log(self.request.user,
                       f'Ended Break\nTotal Break Time: {performance_obj.break_time // 3600}:{(performance_obj.break_time % 3600) // 60}:{(performance_obj.break_time % 3600) % 60}')
            messages.success(request, 'Break Ended')
        return redirect('HR_App:index')


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('HR_App:index')
    template_name = 'HR_App/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        self.on_signup()
        return super().form_valid(form)

    def on_signup(self):
        """
        This function will create a log for the user who just signed up
        :return:
        """
        create_log(self.request.user, 'Signed Up')

        Profile.objects.create(
            user=User.objects.get(username=self.request.POST['username']),
        )
        messages.success(self.request, f'{self.request.POST["username"]} -> Account Created')


class LoginView(TemplateView):
    template_name = 'HR_App/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('HR_App:index')
        return super().get(request, *args, **kwargs)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            self.on_login()
            messages.success(request, 'Logged In')
            return redirect('HR_App:index')
        else:
            messages.error(request, 'Invalid Username or Password', extra_tags='danger')
            return redirect('HR_App:login')

    def on_login(self):
        """
        This function will create a log for the user who just logged in
        :return:
        """
        create_log(self.request.user, 'Logged In')

        # Profile
        try:
            prof = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            prof = Profile.objects.create(
                user=self.request.user
            )
        prof.is_on_break = False
        prof.is_logged_in = True
        prof.save()

        # Performance
        per, _ = Performance.objects.get_or_create(
            user=self.request.user,
            date=datetime.datetime.now().date(),
            defaults={'login_time': datetime.datetime.now().time()}
        )
        per.start_time = datetime.datetime.now().time()
        per.save()


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'HR_App/logout.html'

    def post(self, request):
        self.on_logout(request)
        logout(request)
        return redirect('HR_App:login')

    def on_logout(self, request):
        """
        This function will create a log for the user who just logged out
        :return:
        """

        # Profile
        prof = Profile.objects.get(user=self.request.user)
        was_on_break = prof.is_on_break
        prof.is_on_break = False
        prof.is_logged_in = False
        prof.save()
        try:
            per = Performance.objects.get(user=request.user, date=datetime.datetime.now().date())
        except:
            per = Performance.objects.create(
                user=request.user,
                date=datetime.datetime.now().date(),
                login_time=datetime.datetime.now().time(),
                start_time=datetime.datetime.now().time(),
                end_time=datetime.datetime.now().time(),
            )
        break_start_time = per.break_start_time if per else None
        break_end_time = (
            datetime.datetime.now().time() if was_on_break else
            per.break_end_time if per else None
        )
        break_time = (
            ((break_end_time.hour * 3600) + (break_end_time.minute * 60) + break_end_time.second) -
            ((break_start_time.hour * 3600) + (break_start_time.minute * 60) + break_start_time.second)
            if break_start_time is not None and break_end_time is not None else
            0
        )
        # Calculate the work_time
        per.end_time = datetime.datetime.now().time()
        start = (per.start_time.hour * 3600) + (per.start_time.minute * 60) + per.start_time.second
        end = (per.end_time.hour * 3600) + (per.end_time.minute * 60) + per.end_time.second
        total = end - start
        per.work_time += total - break_time
        per.break_time = 0
        per.save()

        create_log(self.request.user,
                   f'Logged Out\nTotal WorkTime Today: {per.work_time // 3600}H {(per.work_time % 3600) // 60}M {(per.work_time % 3600) % 60}S')
        messages.success(request, 'Logged Out')


class LogsView(LoginRequiredMixin, ListView):
    model = Logs
    template_name = 'HR_App/logs.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return Logs.objects.order_by('-date', '-time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()

        username = self.request.GET.get('username')
        if username:
            context['logs'] = Logs.objects.filter(user__username=username).order_by('-date', '-time')

        return context


class UserStatusView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'HR_App/user_status.html'
    context_object_name = 'profiles'


class AdminView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'HR_App/admin.html'
    context_object_name = 'profiles'

    def post(self, request):
        profile_id = request.POST.get('profile_id')
        user_profile = Profile.objects.get(id=profile_id)
        print(user_profile.is_on_break)
        if user_profile.is_on_break:
            user_profile.is_on_break = False
            user_profile.save()
            break_start_time = Performance.objects.get(user=user_profile.user,
                                                       date=datetime.datetime.now().date()).break_start_time
            break_end_time = datetime.datetime.now().time()
            break_duration = ((break_end_time.hour * 3600) + (break_end_time.minute * 60) + break_end_time.second) - (
                        (break_start_time.hour * 3600) + (break_start_time.minute * 60) + break_start_time.second)
            total_break = break_duration
            per = Performance.objects.get(user=user_profile.user, date=datetime.datetime.now().date())
            per.break_end_time = break_end_time
            per.break_time += total_break
            per.save()
            create_log(
                user_profile.user,
                f'Admin Ended it\'s Break, Total Break Time: {per.break_time // 3600}:{(per.break_time % 3600) // 60}:{(per.break_time % 3600) % 60}'
            )
        else:
            user_profile.is_on_break = True
            user_profile.save()
            break_start_time = datetime.datetime.now().time()
            per = Performance.objects.get(user=user_profile.user, date=datetime.datetime.now().date())
            per.break_start_time = break_start_time
            per.save()
            create_log(user_profile.user, 'Admin Started it\'s Break')
        return redirect('HR_App:admin')


class AttendanceView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'HR_App/attendance.html'
    context_object_name = 'users'


class UserAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'HR_App/user_attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        attendances = Performance.objects.filter(user=user).order_by('-date')

        # Apply filtering based on form data
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        day = self.request.GET.get('day')

        if year:
            attendances = attendances.filter(date__year=year)
        if month:
            attendances = attendances.filter(date__month=month)
        if day:
            attendances = attendances.filter(date__day=day)

        work_time = sum([att.work_time for att in attendances])

        context['performance'] = attendances
        context['user_att'] = user
        context['years'] = Performance.objects.filter(user=user).values_list('date__year', flat=True).distinct()
        context['months'] = Performance.objects.filter(user=user).values_list('date__month', flat=True).distinct()
        context['days'] = Performance.objects.filter(user=user).values_list('date__day', flat=True).distinct()
        context['worktime_hour'] = work_time // 3600
        context['worktime_minute'] = (work_time % 3600) // 60
        context['worktime_second'] = work_time % 3600 % 60

        return context