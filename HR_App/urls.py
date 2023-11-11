from django.urls import path
from HR_App import views

app_name = 'HR_App'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('logs/', views.LogsView.as_view(), name='logs'),
    path('statuspage/', views.UserStatusView.as_view(), name='user_status'),
    path('xceladmin/', views.AdminView.as_view(), name='admin'),
    # # functions paths
    # path('on_break/', views.break_start, name='func_break_start'),
    # path('end_break/', views.break_end, name='func_break_end'),
]