# -*- coding:utf8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from models import ApiHosts
import platform
import os
import time
from api_cloud import errorinfo, data_page, get_ip, public
import json


@login_required
def hosts_list(request):
    public.is_admin(request)
    pagesize = request.GET.get("pagesize", 5)
    hosts_info = ApiHosts.objects.filter(status=1).order_by("-create_time")
    hosts_info, page_range, paginator = data_page.data_page(request,hosts_info, pagesize)
    context = {'hosts_info': hosts_info, "page_range": page_range}
    return render(request, 'hosts_list.html', context)


def hosts_change(request):
    try:
        hosts_id = request.GET.get("hosts_id", 0)
        hosts_content = get_object_or_404(ApiHosts, id=hosts_id, status=1).content
        set_server_hosts(hosts_content)
        other_hosts = ApiHosts.objects.filter().exclude(id=hosts_id)
        for others in other_hosts:
            others.is_current = False
            others.save()
        cur_hosts = get_object_or_404(ApiHosts, id=hosts_id, status=1)
        cur_hosts.is_current = True
        cur_hosts.save()
        return HttpResponseRedirect(reverse("api_hosts:hosts_list"))
    except Exception as ex:
        raise Http404(str(ex))


@csrf_exempt
def hosts_edit_save(request):
    try:
        hosts_id = request.POST.get("hosts_id", 0)
        hosts_id = int(hosts_id)
        hosts_name = request.POST.get("hosts_name", "")
        hosts_content = request.POST.get("hosts_content", "")
        if ApiHosts.objects.filter(name=hosts_name, status=1).exclude(id=hosts_id):
            error_code = 100001
        elif hosts_name == "":
            error_code = 100002
        else:
            edit_hosts = get_object_or_404(ApiHosts, id=hosts_id, status=1)
            edit_hosts.name = hosts_name
            edit_hosts.content = hosts_content
            edit_hosts.save()
            error_code = 0
            if edit_hosts.is_current:
                set_server_hosts(edit_hosts.content)
        heads = {"code": error_code, "message": errorinfo.change_to_message(error_code)}
        result = {"heads": heads}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


def set_server_hosts(hosts_content):
    if "Windows" in platform.platform():
        hosts_file_dir = "C:\Windows\System32\drivers\etc"
    else:
        hosts_file_dir = "/etc"
    os.chdir(hosts_file_dir)
    hosts_file = open("hosts", 'w')
    hosts_file.write(hosts_content.encode("utf8"))
    hosts_file.close()


@csrf_exempt
def hosts_add_save(request):
    try:
        hosts_name = request.POST.get("hosts_name", "")
        hosts_content = request.POST.get("hosts_content", "")
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        new_hosts_id = 0
        if ApiHosts.objects.filter(name=hosts_name, status=1):
            error_code = 100001
        elif hosts_name == "":
            error_code = 100002
        else:
            error_code = 0
            add_hosts = ApiHosts(name=hosts_name, content=hosts_content, create_time=create_time, is_current=False, status=1)
            add_hosts.save()
            new_hosts_id = add_hosts.id
        heads = {"code": error_code, "message": errorinfo.change_to_message(error_code)}
        result = {"heads": heads, "hosts_id": new_hosts_id}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


def hosts_delete(request):
    try:
        hosts_id = request.GET.get("hosts_id", "")
        delete_hosts = get_object_or_404(ApiHosts, id=hosts_id, status=1)
        if delete_hosts.is_current:
            error_code = 100013
        else:
            error_code = 0
            delete_hosts.status = -1
            delete_hosts.save()
        heads = {"code": error_code, "message": errorinfo.change_to_message(error_code)}
        result = {"heads": heads}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as ex:
        raise Http404(str(ex))


@login_required
def hosts_get_detail(request):
    public.is_admin(request)
    try:
        hosts_id = request.GET.get("hosts_id", "")
        hosts_info = get_object_or_404(ApiHosts, id=hosts_id, status=1)
        context = {"hosts_info": hosts_info}
        return render(request, "hosts_detail.html", context)
    except Exception as ex:
        raise Http404(str(ex))


@login_required
def hosts_new_hosts(request):
    public.is_admin(request)
    try:
        hosts_id = request.GET.get("hosts_id", "")
        if hosts_id != "":
            hosts_info = get_object_or_404(ApiHosts, id=hosts_id, status=1)
            context = {"hosts_info": hosts_info}
            return render(request, "hosts_add.html", context)
        else:
            return render(request, "hosts_add.html")
    except Exception as ex:
        raise Http404(str(ex))


@login_required
def hosts_show_current(request):
    try:
        if "Windows" in platform.platform():
            hosts_file_dir = "C:\Windows\System32\drivers\etc"
        else:
            hosts_file_dir = "/etc"
        os.chdir(hosts_file_dir)
        hosts_file_object = open("hosts")
        hosts_file = hosts_file_object.readlines()
        context = {"cur_hosts": hosts_file, "cur_ip": get_ip.get_ip()}
        return render(request, "hosts_current.html", context)
    except Exception as ex:
        raise Http404(str(ex))






