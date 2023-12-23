from django.urls import path
from HR_App import views

app_name = 'HR_App'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logs/', views.LogsView.as_view(), name='logs'),
    path('statuspage/', views.UserStatusView.as_view(), name='user_status'),
    path('xceladmin/', views.AdminView.as_view(), name='admin'),
    path('attendance/', views.AttendanceView.as_view(), name='attendance'),
    path('attendance/user/<int:user_id>/', views.UserAttendanceView.as_view(), name='attendance_user'),
    # # functions paths
    # path('on_break/', views.break_start, name='func_break_start'),
    # path('end_break/', views.break_end, name='func_break_end'),
]