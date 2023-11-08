from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', index, name='main'),
    path('result/', views.result_view, name='result_view_name')
]
