# -*- coding:utf8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


def is_admin(request):
    uid = request.session["uid"]
    get_object_or_404(User, id=uid, is_superuser=True, is_active=1)


def is_normal_user(request):
    uid = request.session["uid"]
    get_object_or_404(User, id=uid, is_superuser=False, is_active=1)
