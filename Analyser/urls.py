# analyzer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_and_analyze, name='upload_and_analyze'),
]