# -*- coding:utf8 -*-
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from api_cloud import errorinfo
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@csrf_exempt
# 登录接口，登录后uid写入session中
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            uid = user.id
            request.session["uid"] = uid
            redirect_url = request.GET.get('next')
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
            elif user.is_superuser:
                return HttpResponseRedirect(reverse("api_user:user_list"))
            else:
                return HttpResponseRedirect(reverse("api_api:api_list"))
        else:
            error_code = 100000
            message = errorinfo.change_to_message(error_code)
            return render_to_response("user_login.html",
                                      context_instance=RequestContext(request, {"error_user": True,
                                                                                "error_message": message}))
    return render_to_response("user_login.html")


# 注销接口，删除session中的uid
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("api_user:user_login"))


@login_required
# 首页
def home(request):
    try:
        uid = request.session["uid"]
        user = User.objects.get(id=uid)
        if user:
            if user.is_superuser:
                return HttpResponseRedirect(reverse("api_user:user_list"))
            else:
                return HttpResponseRedirect(reverse("api_api:api_list"))
        else:
            return HttpResponseRedirect(reverse("api_user:user_login"))
    except KeyError:
        return HttpResponseRedirect(reverse("api_user:user_login"))


def user_get_real_name(request):
    try:
        uid = request.session["uid"]
        user = User.objects.get(id=uid)
        if user:
            real_name = user.first_name
            return HttpResponse(real_name)
        else:
            return HttpResponseRedirect(reverse("api_user:user_login"))
    except KeyError:
        return HttpResponseRedirect(reverse("api_user:user_login"))




