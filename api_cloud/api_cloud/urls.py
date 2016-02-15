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
from django.conf.urls import include, url
from django.contrib import admin
from api_user import urls as user_urls
from api_api import urls as api_urls
from api_hosts import urls as hosts_urls
from api_project import urls as project_urls
from api_user import login


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login.home, name="home"),
    url(r'^api/home/', login.home, name="home"),
    url(r'^api/user/', include(user_urls, namespace="api_user")),
    url(r'^api/api/', include(api_urls, namespace="api_api")),
    url(r'^api/hosts/', include(hosts_urls, namespace="api_hosts")),
    url(r'^api/project/', include(project_urls, namespace="api_project")),
]
