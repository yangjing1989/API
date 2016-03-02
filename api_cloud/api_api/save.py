# -*- coding:utf8 -*-
import time
from models import ApiApi
from api_cloud import errorinfo


# 保存公用方法
def public_save(request):
    uid = request.session.get('uid')
    api_id = request.POST.get("api_id", "")
    api_name = request.POST.get("api_name", "")
    api_url = request.POST.get("api_url", "")
    url_list = request.POST.get("url_list", "")
    api_domain = request.POST.get("api_domain", "")
    api_http_type = request.POST.get("api_http_type", 0)
    api_method = request.POST.get("api_method", 0)
    api_headers = request.POST.get("api_headers", "")
    api_body_type = request.POST.get("api_body_type", "")
    project_id = request.POST.get("project_id", 1)
    if api_body_type == "":
        api_body_type = None
    api_body_value = request.POST.get("api_body_value", "")
    api_remarks = request.POST.get("api_remarks", "")
    api_result = request.POST.get("api_result", "")
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    result = {}
    heads = {}
    if api_name == "":
        error_code = 100004
    else:
        if api_id:
            update_api = ApiApi.objects.get(id=api_id)
            try:
                error_code = 0
                update_api.name = api_name
                update_api.api_http_type = api_http_type
                update_api.api_url = api_url
                update_api.url_list = url_list
                update_api.api_domain = api_domain
                update_api.api_method = api_method
                update_api.api_headers = api_headers
                update_api.api_body_type = api_body_type
                update_api.api_body_value = api_body_value
                update_api.remarks = api_remarks
                update_api.creater = uid
                update_api.update_time = create_time
                update_api.api_expect_result = api_result
                update_api.save()
                api_id = update_api.id
                result["api_id"] = api_id
            except Exception as ex:
                heads["exception"] = str(ex)
                error_code = 110000
        else:
            if api_result != "":
                last_execute_time = create_time
            else:
                last_execute_time = None
            add_api = ApiApi(name=api_name,
                             api_http_type=api_http_type, api_url=api_url, project_id=project_id,
                             url_list=url_list, api_domain=api_domain,
                             api_method=api_method, api_headers=api_headers,
                             api_body_type=api_body_type, api_body_value=api_body_value,
                             remarks=api_remarks, create_time=create_time, api_expect_result=api_result,
                             update_time=create_time, creater=uid, last_execute_time=last_execute_time, status=1)
            try:
                error_code = 0
                add_api.save()
                add_api_id = add_api.id
                result["api_id"] = add_api_id
            except Exception as ex:
                heads["exception"] = str(ex)
                error_code = 110000
                print ex

    heads["code"] = error_code
    heads["message"] = errorinfo.change_to_message(error_code)
    result["heads"] = heads
    return result
