# coding=utf-8
from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^date_pererabotka/', views.get_per, name='get_per'),
    url(r'^pererabotka/(?P<date_per>\d{4}-\d{2}-\d{2})/', views.get_per2, name='get_per2'),
    url(r'^addpererabotka/', views.add_per, name='add_per'),
    url(r'^page/(\d+)/$', views.get_per, name='get_per'),
    url(r'^', views.get_start, name='get_start'),

]
