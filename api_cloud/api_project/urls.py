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
from api_project import project


urlpatterns = [
    url(r'^list/', project.project_list, name="project_list"),
    url(r'^new/', project.project_new, name="project_new"),
    url(r'^detail/', project.project_detail, name="project_detail"),
    url(r'^add/', project.project_add, name="project_add"),
    url(r'^edit/', project.project_edit, name="project_edit"),
    url(r'^del/', project.project_delete, name="project_del"),
    url(r'^tree/', project.all_project_tree, name="project_tree"),
    url(r'^user_tree/', project.user_project_tree, name="project_user_tree"),
    url(r'per_tree/', project.user_permission_project_tree, name="project_per_tree"),
]
