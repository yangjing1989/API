# -*- coding:utf8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from api_cloud import errorinfo, data_page, public
from django.contrib.auth.decorators import login_required
from models import ApiApi
from api_project.models import ApiProject
from api_user.models import Permission
from django.contrib.auth.models import User
import json
import save
import execute
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


@login_required
# 获取接口列表
def api_list(request):
    public.is_normal_user(request)
    uid = request.session["uid"]
    context = {'uid': uid}
    return render(request, 'api_list.html', context)


@login_required
# 跳转至新建页面
def api_new(request):
    public.is_normal_user(request)
    try:
        project_id = request.GET.get("project_id", "")
        api_id = request.GET.get("api_id", "")
        if api_id != "":
            api_info = get_object_or_404(ApiApi, id=api_id, status=1)
            if int(api_info.project_id) in get_uid_permission(request.session["uid"]):
                project_name = get_object_or_404(ApiProject, id=api_info.project_id, status=1).name
                context = {'api_info': api_info, "project_name": project_name}
                return render(request, 'api_new.html', context)
            else:
                raise Http404("没有权限")
        elif project_id != "":
            per_list = get_uid_permission(request.session["uid"])
            project_id = int(project_id)
            if project_id in per_list:
                project_name = get_object_or_404(ApiProject, id=project_id, status=1).name
                context = {'project_id': project_id, "project_name": project_name}
                return render(request, 'api_new.html', context)
            else:
                raise Http404("没有权限")
    except Exception as ex:
        raise Http404(str(ex))


@csrf_exempt
# 新建保存
def api_add_save(request):
    result = save.public_save(request)
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
# 编辑保存
def api_edit_save(request):
    result = save.public_save(request)
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
# 跳转至接口详情页面
def api_detail(request):
    public.is_normal_user(request)
    try:
        api_id = request.GET.get("api_id", "")
        api_info = get_object_or_404(ApiApi, id=api_id, status=1)
        if int(api_info.project_id) in get_uid_permission(request.session["uid"]):
            project_name = get_object_or_404(ApiProject, id=api_info.project_id, status=1).name
            context = {'api_info': api_info, "project_name": project_name}
            return render(request, 'api_detail.html', context)
        else:
            raise Http404("没有权限")
    except Exception as ex:
        raise Http404(str(ex))


@csrf_exempt
# 删除
def api_delete(request):
    try:
        uid = request.session["uid"]
        all_api_list = request.POST.get("api_list", "")
        error_code = 0
        if all_api_list != "":
            all_api_list = all_api_list.split(",")
            api_info = ApiApi.objects.filter(id__in=all_api_list)
            for api in api_info:
                if int(api.creater) == int(uid):
                    api.status = -1
                    api.save()
                    error_code = 0
                else:
                    error_code = 100027
        heads = {"code": error_code, "message": errorinfo.change_to_message(error_code)}
        result = {"heads": heads}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


@csrf_exempt
# 获取请求的结果
def api_get_execute_result(request):
    result = execute.exe_result(request)
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
# 获取批量请求的结果
def api_get_batch_execute_result(request):
    result = execute.exe_batch_result(request)
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def api_batch_move(request):
    try:
        all_api_list = request.POST.get("api_list", "")
        heads = {}
        error_code = 0
        project_id = request.POST.get("project_id", "")
        if all_api_list != "" and project_id != "":
            all_api_list = all_api_list.split(",")
            api_info = ApiApi.objects.filter(id__in=all_api_list)
            for api in api_info:
                try:
                    api.project_id = project_id
                    api.save()
                except Exception as ex:
                    heads["exceptions"] = str(ex)
                    error_code = 110000
        heads = {"code": error_code, "message": errorinfo.change_to_message(error_code)}
        result = {"heads": heads}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


# 获取用户有权限的项目
def get_uid_permission(uid):
    permissions = Permission.objects.filter(user_id=uid)
    permission_list = []
    for permission in permissions:
        permission_list.append(int(permission.project_id))
        son_info = ApiProject.objects.filter(parent_id=permission.project_id, status=1)
        if son_info:
            for son in son_info:
                permission_list.append(int(son.id))
                sun_info = ApiProject.objects.filter(parent_id=son.id, status=1)
                if sun_info:
                    for sun in sun_info:
                        permission_list.append(int(sun.id))
    return permission_list


def get_api_data(request):
    try:
        project_id = request.GET.get("project_id", "")
        pagesize = request.GET.get("pagesize", 10)
        if project_id != "":
            all_api_info = ApiApi.objects.filter(project_id=project_id, status=1).order_by("-create_time")
            all_api_info, page_range, paginator = data_page.data_page(request, all_api_info, pagesize)
            result = []
            for api_info in all_api_info:
                creater = get_object_or_404(User, id=api_info.creater, is_active=1).first_name
                if api_info.api_method == 1:
                    method = "GET"
                else:
                    method = "POST"

                data = {"id": api_info.id, "name": api_info.name,
                        "api_url": api_info.api_url, "api_domain": api_info.api_domain, "creater": creater,
                        "api_method": method, "api_is_success": api_info.api_is_success}
                result.append(data)
            result_data = {"data": result, "page_range": page_range,
                           "pages": paginator.num_pages, "counts": paginator.count}
        else:
            result_data = {"data": "", "page_range": "",
                           "pages": 1, "counts": 0}
        return HttpResponse(json.dumps(result_data), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))






