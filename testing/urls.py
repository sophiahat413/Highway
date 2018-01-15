"""testing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from data.views import filiter,delete_data,show,test,check,mapp,user_info,database_info,home_page,get_data
from data.views import type_data, get_signalmap,get_statictics,statisticsSelect

from data.views import hello_world

#from data.views import testtt

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', home_page),
    url(r'^index/getDataList/$',get_data),
    url(r'^index/getSignalMap/$',get_signalmap),
    url(r'^getDataList/$',type_data),
    url(r'^index/statisticsPage/$',get_statictics),
    url(r'^statisticsSelect/$',statisticsSelect),
    url(r'^hello/$', hello_world),
    url(r'^filter/$', filiter),
    url(r'^user/$',user_info),
    url(r'^database/$', database_info),
    #url(r'^change_map/$',change_map),
    #url(r'^add/$',add_data),
    url(r'^delete/$',delete_data),
    url(r'^show/', show),
    url(r'^test/$', test),
    url(r'^check/$', check),
    url(r'^mapp/$', mapp),
]
