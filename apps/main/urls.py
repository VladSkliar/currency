# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^currencies/', views.currencies, name='currencies'),
    url(r'^currency/$', views.currency, name='currency'),
    url(r'^currency/(?P<currency_name>[A-Za-z]+)/$',
        views.currency, 
        name='currency'),
    url(r'^currency/(?P<currency_name>[A-Za-z]+)/(?P<curr_value>[A-Za-z]+)/$',
        views.currency, 
        name='currency'),
    url(r'^sequence/', views.sequence, name='sequence'),
]