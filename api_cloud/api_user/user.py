# -*- coding:utf8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from api_cloud import errorinfo, data_page, public
from api_project.models import ApiProject
from models import Permission
from django.contrib.auth.decorators import login_required
import json


@login_required
# 用户列表
def user_list(request):
    public.is_admin(request)
    pagesize = request.GET.get("pagesize", 10)
    user_info = User.objects.filter(is_active=1).order_by("-id")
    user_info, page_range, paginator = data_page.data_page(request, user_info, pagesize)
    context = {'user_info': user_info, "page_range": page_range}
    return render(request, 'user_list.html', context)


@login_required
def user_new(request):
    public.is_admin(request)
    return render(request, 'user_new.html')


@csrf_exempt
def user_add(request):
    result = public_save(request)
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def user_edit(request):
    result = public_save(request)
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def user_detail(request):
    public.is_admin(request)
    user_id = request.GET.get("user_id", "")
    user_info = get_object_or_404(User, id=user_id, is_active=1)
    project_info = ApiProject.objects.filter(status=1).order_by("create_time")
    permission_info = Permission.objects.filter(user_id=user_id)
    context = {'user_info': user_info, "project_info": project_info, "permission_info": permission_info}
    return render(request, 'user_detail.html', context)


def user_delete(request):
    head = {}
    uid = request.session["uid"]
    try:
        user_id = request.GET.get("user_id", "")
        if int(user_id) == int(uid):
            error_code = 100026
        else:
            user_info = get_object_or_404(User, id=user_id, is_active=1)
            try:
                user_info.is_active = 0
                user_info.save()
                Permission.objects.filter(user_id=user_id).delete()
                error_code = 0
            except Exception as ex:
                error_code = 110000
                head["exception"] = ex
        head["code"] = error_code
        head["message"] = errorinfo.change_to_message(error_code)
        result = {"heads": head}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


def public_save(request):
    user_id = request.POST.get("user_id", "")
    user_name = request.POST.get("user_name", "")
    user_real_name = request.POST.get("user_real_name", "")
    user_email = request.POST.get("user_email", "")
    user_password = request.POST.get("user_password", "")
    user_re_password = request.POST.get("user_re_password", "")
    user_is_admin = request.POST.get("user_is_admin", 0)
    permission_list = request.POST.get("permission_list", "")
    if user_is_admin == 1 or user_is_admin == "1":
        user_is_admin = True
    else:
        user_is_admin = False
    result = {}
    head = {}
    if user_name == "":
        error_code = 100015
    elif user_password == "" or user_re_password == "":
        error_code = 100021
    elif user_password != user_re_password:
        error_code = 100019
    elif len(user_password) < 6:
        error_code = 100020
    else:
        new_user_id = ""
        if user_id == "":
            if User.objects.filter(username=user_name, is_active=1):
                error_code = 100017
            else:
                add_user = User(username=user_name, first_name=user_real_name, is_superuser=user_is_admin, email=user_email)
                try:
                    add_user.set_password(user_password)
                    add_user.save()
                    new_user_id = add_user.id
                    error_code = 0
                except Exception as ex:
                    head["exceptions"] = ex
                    error_code = 110000
        else:
            if User.objects.filter(username=user_name, is_active=1).exclude(id=user_id):
                error_code = 100017
            else:
                edit_user = get_object_or_404(User, id=user_id)
                try:
                    edit_user.username = user_name
                    edit_user.first_name = user_real_name
                    edit_user.email = user_email
                    if user_password != edit_user.password:
                        edit_user.set_password(user_password)
                    edit_user.is_superuser = user_is_admin
                    edit_user.save()
                    new_user_id = user_id
                    error_code = 0
                except Exception as ex:
                    head["exceptions"] = ex
                    error_code = 110000
        # 保存权限
        if new_user_id != "":
            permissions = Permission.objects.filter(user_id=new_user_id)
            if permissions:
                for pers in permissions:
                    pers.delete()
            if permission_list != "":
                permission_list = permission_list.encode("utf8")
                permission_list = permission_list.split(",")
                for permission_id in permission_list:
                    permission_info = Permission.objects.filter(user_id=new_user_id, project_id=permission_id)
                    if permission_info:
                        pass
                    else:
                        new_permission = Permission(user_id=new_user_id, project_id=permission_id)
                        new_permission.save()
    head["code"] = error_code
    head["message"] = errorinfo.change_to_message(error_code)
    result["heads"] = head
    return result


@login_required
def user_modify_password(request):
    return render_to_response("user_modify_password.html")


@csrf_exempt
def user_save_password(request):
    old_password = request.POST.get("old_password", "")
    new_password = request.POST.get("new_password", "")
    re_new_password = request.POST.get("re_new_password", "")
    result = {}
    head = {}
    if old_password == "" or new_password == "" or re_new_password == "":
        error_code = 100021
    elif new_password != re_new_password:
        error_code = 100019
    elif len(new_password) < 6:
        error_code = 100020
    else:
        uid = request.session["uid"]
        user = User.objects.get(id=uid)
        if user:
            if user.check_password(old_password):
                try:
                    user.set_password(new_password)
                    user.save()
                    error_code = 0
                except Exception as ex:
                    head["exceptions"] = ex
                    error_code = 110000
            else:
                error_code = 100023
        else:
            error_code = 100018
    head["code"] = error_code
    head["message"] = errorinfo.change_to_message(error_code)
    result["heads"] = head
    return HttpResponse(json.dumps(result), content_type='application/json')



