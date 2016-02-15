"""api_cloud URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from api_hosts import hosts

urlpatterns = [
    url(r'^list/', hosts.hosts_list, name="hosts_list"),
    url(r'^change/', hosts.hosts_change, name="hosts_change"),
    url(r'^new/', hosts.hosts_new_hosts, name="hosts_new"),
    url(r'^add/', hosts.hosts_add_save, name="hosts_add"),
    url(r'^edit/', hosts.hosts_edit_save, name="hosts_edit"),
    url(r'^del/', hosts.hosts_delete, name="hosts_del"),
    url(r'^detail/', hosts.hosts_get_detail, name="hosts_detail"),
    url(r'^current/', hosts.hosts_show_current, name="hosts_current"),
]
