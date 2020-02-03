from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from .views import (UserCreateView, UserDeleteView, UserDetailView, UserListView, UserUpdateView, SendEmailView)

urlpatterns = [
    path('users/', TemplateView.as_view(template_name='Test/main.html'), name='home'),
    path('users/list/', UserListView.as_view(), name='list'),
    path('users/create/', UserCreateView.as_view(), name='create'),
    path('users/update/<int:pk>', UserUpdateView.as_view(), name='update'),
    path('users/delete/<int:pk>', UserDeleteView.as_view(), name='delete'),
    path('users/<int:pk>', UserDetailView.as_view(), name='detail'),
    path('users/send/', SendEmailView.as_view(), name='send'),
    path('users/task/<str:task_id>/', SendEmailView.as_view(), name='task'),
]
