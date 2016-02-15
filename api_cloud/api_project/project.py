# -*- coding:utf8 -*-

import json
from django.shortcuts import render,get_object_or_404
from models import ApiProject
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from api_cloud import errorinfo, data_page, public
from django.contrib.auth.decorators import login_required
from api_api.models import ApiApi
from api_user.models import Permission


@login_required
def project_list(request):
    public.is_admin(request)
    pagesize = request.GET.get("pagesize", 10)
    project_info = ApiProject.objects.filter(status=1).order_by("-create_time")
    project_info, page_range, paginator = data_page.data_page(request, project_info, pagesize)
    context = {'project_info': project_info, "page_range": page_range}
    return render(request, 'project_list.html', context)


@login_required
def project_new(request):
    public.is_admin(request)
    return render(request, 'project_new.html')


@login_required
def project_detail(request):
    public.is_admin(request)
    try:
        project_id = request.GET.get("project_id", "")
        project_info = get_object_or_404(ApiProject, id=project_id, status=1)
        context = {'project_info': project_info}
        return render(request, 'project_detail.html', context)
    except Exception as ex:
        raise Http404(str(ex))


@csrf_exempt
def project_add(request):
    result = public_save(request)
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def project_edit(request):
    result = public_save(request)
    return HttpResponse(json.dumps(result), content_type='application/json')


def project_delete(request):
    try:
        project_id = request.GET.get("project_id", "")
        if ApiApi.objects.filter(project_id=project_id, status=1):
            error_code = 100024
        elif ApiProject.objects.filter(parent_id=project_id, status=1):
            error_code = 100028
        else:
            del_project = get_object_or_404(ApiProject, id=project_id, status=1)
            del_project.status = -1
            del_project.save()
            error_code = 0
        heads = {"code": error_code, "message": errorinfo.change_to_message(error_code)}
        result = {"heads": heads}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


def public_save(request):
    try:
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        project_id = request.POST.get("project_id", "")
        parent_project_id = request.POST.get("parent_project_id", "")
        api_document = request.POST.get("api_document","")
        project_name = request.POST.get("project_name", "")
        project_level = request.POST.get("project_level", 0)
        if project_name == "":
            # 无论添加还是编辑都名称都不能为空
            error_code = 100012
        else:
            if parent_project_id == "":
                project_level = 1
            else:
                project_level = int(project_level)+1
            # 有project_id表示是编辑
            if project_id != "":
                if ApiProject.objects.filter(name=project_name, status=1).exclude(id=project_id):
                    error_code = 100013
                else:
                    edit_project = get_object_or_404(ApiProject, id=project_id, status=1)
                    edit_project.name = project_name
                    edit_project.api_document = api_document
                    if parent_project_id != "":
                        edit_project.parent_id = int(parent_project_id)
                        edit_project.level = project_level
                    edit_project.save()
                    error_code = 0
                # 无project_id表示是添加
            else:
                if ApiProject.objects.filter(name=project_name, status=1):
                    error_code = 100013
                else:
                    if parent_project_id != "":
                        parent_project_id = int(parent_project_id)
                    else:
                        parent_project_id = None
                    new_project = ApiProject(name=project_name, parent_id=parent_project_id,
                                             level=project_level, api_document=api_document,
                                             create_time=create_time)
                    new_project.save()
                    error_code = 0
        heads = {"code": error_code, "message": errorinfo.change_to_message(error_code)}
        result = {"heads": heads}
        return result
    except Exception as ex:
        raise Http404(str(ex))


@csrf_exempt
def all_project_tree(request):
    try:
        project_id = request.POST.get("project_id", "")
        selected_parent_id = ""
        if project_id != "":
            if ApiProject.objects.filter(id=project_id, status=1):
                selected_parent_id = ApiProject.objects.get(id=project_id).parent_id
                if selected_parent_id is None:
                    selected_parent_id = ""
        all_root_project = ApiProject.objects.filter(parent_id=None, status=1).order_by("-create_time")
        root = []
        if all_root_project:
            for root_project in all_root_project:
                # 得到二级项目
                all_second_project = ApiProject.objects.filter(parent_id=int(root_project.id), level=2, status=1)
                second_data = []
                if all_second_project:
                    for second_project in all_second_project:
                        # 得到三级项目
                        all_third_project = ApiProject.objects.filter(parent_id=int(second_project.id), level=3, status=1)
                        third_data = []
                        if all_third_project:
                            for third_project in all_third_project:
                                third = {"id": str(third_project.id), "pId": str(second_project.id),
                                         "name": third_project.name, "open": "true", "nocheck": "true"}
                                third_data.append(third)
                        second = {"id": str(second_project.id), "pId": str(root_project.id),
                                  "name": second_project.name, "open": "true", "children": third_data}

                        if selected_parent_id != "":
                            if int(second_project.id) == int(selected_parent_id):
                                second["checked"] = "true"
                        second_data.append(second)
                root_data = {"id": str(root_project.id), "name": root_project.name, "open": "true", "children": second_data}
                if selected_parent_id != "":
                    if int(root_project.id) == int(selected_parent_id):
                        root_data["checked"] = "true"
                root.append(root_data)
            result = root
        else:
            result = ""
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


@csrf_exempt
def user_project_tree(request):
    try:
        user_id = request.POST.get("user_id", "")
        permission_list = []
        if user_id != "":
            if Permission.objects.filter(user_id=user_id):
                all_per_list = Permission.objects.filter(user_id=user_id)
                for per_list in all_per_list:
                    permission_list.append(per_list.project_id)
        all_root_project = ApiProject.objects.filter(parent_id=None, status=1).order_by("-create_time")
        root = []
        if all_root_project:
            for root_project in all_root_project:
                root_data = {"id": str(root_project.id), "name": root_project.name, "open": "true"}
                if permission_list != "":
                    if int(root_project.id) in permission_list:
                        root_data["checked"] = "true"
                root.append(root_data)
            result = root
        else:
            result = ""
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


@csrf_exempt
def user_permission_project_tree(request):
    try:
        user_id = request.POST.get("user_id", "")
        result = ""
        permission_list = []
        if user_id != "":
            if Permission.objects.filter(user_id=user_id):
                all_per_list = Permission.objects.filter(user_id=user_id)
                for per_list in all_per_list:
                    permission_list.append(per_list.project_id)
            all_root_project = ApiProject.objects.filter(id__in=permission_list, parent_id=None, status=1).order_by("-create_time")
            root = []
            if all_root_project:
                for root_project in all_root_project:
                    # 得到二级项目
                    all_second_project = ApiProject.objects.filter(parent_id=int(root_project.id), level=2, status=1)
                    second_data = []
                    if all_second_project:
                        for second_project in all_second_project:
                            # 得到三级项目
                            all_third_project = ApiProject.objects.filter(parent_id=int(second_project.id), level=3, status=1)
                            third_data = []
                            if all_third_project:
                                for third_project in all_third_project:
                                    third = {"id": str(third_project.id), "pId": str(second_project.id),
                                             "name": third_project.name, "open": "true"}
                                    third_data.append(third)
                            second = {"id": str(second_project.id), "pId": str(root_project.id),
                                      "name": second_project.name, "open": "true", "children": third_data}
                            second_data.append(second)
                    root_data = {"id": str(root_project.id), "name": root_project.name, "open": "true",
                                 "children": second_data}
                    root.append(root_data)
                result = root
            else:
                result = ""
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))
