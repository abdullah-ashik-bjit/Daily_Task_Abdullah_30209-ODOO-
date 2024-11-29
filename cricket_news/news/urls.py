from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib import messages
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news_list, name='news_list'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=None,
        extra_context={
            'error_message': 'Invalid username or password'
        }
    ), name='login'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('create_news/', views.create_news, name='create_news'),
    path('news/<int:pk>/edit/', views.edit_news, name='edit_news'),
]