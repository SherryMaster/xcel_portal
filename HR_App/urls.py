from django.urls import path
from HR_App import views

app_name = 'HR_App'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logs/', views.LogsView.as_view(), name='logs'),
]