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
import api_user.login
import api_user.user

urlpatterns = [
    url(r'^real/', api_user.login.user_get_real_name, name="user_real_name"),
    url(r'^login/', api_user.login.user_login,  name="user_login"),
    url(r'^logout/', api_user.login.user_logout, name="user_logout"),
    url(r'^list/', api_user.user.user_list, name="user_list"),
    url(r'^new/', api_user.user.user_new, name="user_new"),
    url(r'^add/', api_user.user.user_add, name="user_add"),
    url(r'^edit/', api_user.user.user_edit, name="user_edit"),
    url(r'^detail/', api_user.user.user_detail, name="user_detail"),
    url(r'^del/', api_user.user.user_delete, name="user_del"),
    url(r'^password/', api_user.user.user_modify_password, name="user_password"),
    url(r'^modify/', api_user.user.user_save_password, name="user_modify"),
]
