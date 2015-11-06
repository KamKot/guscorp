from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^', 'loginsys.views.login'),
    url(r'^login/', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
]
