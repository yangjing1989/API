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
from api_api import api

urlpatterns = [
    url(r'^list/', api.api_list, name="api_list"),
    url(r'^data/', api.get_api_data, name="api_data"),
    url(r'^new/', api.api_new, name="api_new"),
    url(r'^add/', api.api_add_save, name="api_add"),
    url(r'^detail/', api.api_detail, name="api_detail"),
    url(r'^edit/', api.api_edit_save, name="api_edit"),
    url(r'^del/', api.api_delete, name="api_del"),
    url(r'^result/', api.api_get_execute_result, name="api_result"),
    url(r'^batch/', api.api_get_batch_execute_result, name="api_batch"),
    url(r'^move/', api.api_batch_move, name="api_move"),
]
