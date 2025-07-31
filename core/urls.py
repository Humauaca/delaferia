from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import forms

app_name = 'core'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=forms.LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]