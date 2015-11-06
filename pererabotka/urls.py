# coding=utf-8
from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^pererabotka/', views.get_per, name='get_per'),
    url(r'^addpererabotka/', views.add_per, name='add_per'),
    url(r'^page/(\d+)/$', views.get_per, name='get_per'),
    url(r'^', views.get_start, name='get_start'),

]
