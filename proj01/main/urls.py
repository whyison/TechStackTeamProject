from django.urls import path
from .views import *
from . import views

app_name = 'main'

urlpatterns = [
    path('', index, name='main'),
    path('result/', views.result_view, name='result_view'),
    path('get_sigg_list/', get_sigg_list, name='get_sigg_list'),
]
