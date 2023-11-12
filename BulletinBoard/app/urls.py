"""
URL configuration for BulletinBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, Responses, AcceptResponse, DeclineResponse, DeleteResponse
app_name = 'app'

urlpatterns = [
    path('', PostsList.as_view(), name='feed'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'), # Ссылка на детали поста
    path('add/', PostCreateView.as_view(), name='post_create'), # Ссылка на создание поста
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'), # Ссылка на редактирование поста
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'), # Ссылка на удаеление поста
    path('responses/', Responses.as_view(), name='responses'),
    path('responses/<int:pk>/accept', AcceptResponse, name='accept_response'),
    path('responses/<int:pk>/decline', DeclineResponse, name='decline_response'),
    path('responses/<int:pk>/delete', DeleteResponse, name='delete_response'),     
]
