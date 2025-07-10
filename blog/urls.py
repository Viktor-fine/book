"""Определяет схемы url для blog"""
from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'), # Список всех тем
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),# Новая тема
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'), # Новая статья по теме
]
