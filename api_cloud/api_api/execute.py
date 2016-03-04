# -*- coding:utf8 -*-
from api_cloud import errorinfo
import json
import httplib
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from api_api.models import ApiApi
import time
import urllib
import re


# 获取请求参数
def get_request_parameters(api_url, url_list, api_domain, api_http_type,
                           api_method, api_headers, api_body_type, api_body_value):
    re_url = ""
    domain_start = api_domain.split("//")[0]
    if domain_start == "http:" or domain_start == "https:":
        pass
    else:
        if api_http_type == 2 or api_http_type == "2":
            re_url += "https://"
        else:
            re_url += "http://"
    re_url += api_domain
    re_url += api_url
    if url_list != "":
        if re_url[len(re_url)-1:] != "?":
            re_url += "?"
        url_list = url_list.encode("utf-8")
        all_urls = url_list.split(',')
        for urls in all_urls:
            urls = json.loads(urls)
            for keys in urls:
                re_url += "&"+keys+"="+urls[keys]

    if api_method == "2" or api_method == 2:
        re_method = "POST"
    else:
        re_method = "GET"

    if api_headers != "":
        api_headers = api_headers.encode("utf-8")
        api_headers = api_headers.replace("}", "").replace("{", "")
        api_headers = "{"+api_headers+"}"
        api_headers = json.loads(api_headers)
    if api_body_value != "":
        api_body_value = api_body_value.encode("utf-8")
        if api_body_type == 3 or api_body_type == "3":
            all_body_keys = api_body_value.split(",")
            api_body = {}
            for all_body_key in all_body_keys:
                body_keys = json.loads(all_body_key)
                for keys in body_keys:
                    api_body[keys] = body_keys[keys]
            api_body_value = urllib.urlencode(api_body)
        elif api_body_type == 2 or api_body_type == "2":
            api_body_value = json.loads(api_body_value)
            api_body_value = json.JSONEncoder().encode(api_body_value)
        elif api_body_type == 1 or api_body_type == "1":
            all_body_keys = api_body_value.split(",")
            api_body = {}
            for all_body_key in all_body_keys:
                body_keys = json.loads(all_body_key)
                for keys in body_keys:
                    api_body[keys] = body_keys[keys]
            api_body_value = api_body
    parameters_list = {"api_domain": api_domain, "api_url": re_url, "api_method": re_method,
                       "api_headers": api_headers, "api_body_type": api_body_type, "api_body_value": api_body_value}
    return parameters_list


def exe_result(request):
    api_url = request.POST.get("api_url", "")
    url_list = request.POST.get("url_list", "")
    api_domain = request.POST.get("api_domain", "")
    api_http_type = request.POST.get("api_http_type", 1)
    api_method = request.POST.get("api_method", 1)
    api_headers = request.POST.get("api_headers", "")
    api_body_type = request.POST.get("api_body_type")
    api_body_value = request.POST.get("api_body_value", "")
    api_id = request.POST.get("api_id", "")
    result = execute(api_url,url_list,api_domain,api_http_type,api_method,api_headers,api_body_type,api_body_value,api_id)
    return result


def exe_batch_result(request):
    api_list = request.POST.get("api_list", "")
    result = ""
    if api_list != "":
        api_list = api_list.split(",")
        not_same = 0
        failed_count = 0
        success_count = 0
        for apis in api_list:
            apis = int(apis)
            if ApiApi.objects.filter(id=apis):
                api_info = ApiApi.objects.get(id=apis)
                result = execute(api_info.api_url, api_info.url_list, api_info.api_domain,
                                 api_info.api_http_type, api_info.api_method,
                                 api_info.api_headers, api_info.api_body_type,
                                 api_info.api_body_value, apis)
                if int(result["heads"]["is_success"]) == 1:
                    success_count += 1
                elif int(result["heads"]["is_success"]) == -1:
                    failed_count += 1
                elif int(result["heads"]["is_success"]) == 0:
                    not_same += 1
                result["failed_count"] = failed_count
                result["success_count"] = success_count
                result["not_same"] = not_same
    return result


def execute(api_url,url_list,api_domain,api_http_type,api_method,api_headers,api_body_type,api_body_value,api_id):
    parameters = get_request_parameters(api_url,url_list,api_domain,api_http_type,api_method,api_headers,api_body_type,api_body_value)
    domain = parameters["api_domain"]
    if domain.split("//")[0] == "http:" or domain.split("//")[0] == "https:":
        domain = domain.split("//")[1]
    url = parameters["api_url"]
    method = parameters["api_method"]
    headers = parameters["api_headers"]
    body_type = parameters["api_body_type"]
    body_value = parameters["api_body_value"]
    result = {}
    heads = {"is_success": ""}

    # 必填项没有时，则显示错误
    if url == "":
        error_code = 100007
    elif domain == "":
        error_code = 100008
    else:
        try:
            if body_type == "1" or body_type == 1:
                register_openers()
                datagen, re_headers = multipart_encode(body_value)
                api_request = urllib2.Request(url, datagen, re_headers)
                if headers != "":
                    for keys in headers:
                        api_request.add_header(keys, headers[keys])
                response = urllib2.urlopen(api_request)
                result_data = response.read()
                http_code = response.code
            else:
                if api_http_type == 2 or api_http_type == "2":
                    connection = httplib.HTTPSConnection(domain)
                else:
                    connection = httplib.HTTPConnection(domain)
                if headers == "":
                    connection.request(method=method, url=url, body=body_value)
                else:
                    connection.request(method=method, url=url, headers=headers, body=body_value)
                response = connection.getresponse()
                http_code = response.status
                result_data = response.read()
            error_code = 0
            result["datas"] = json.dumps(result_data)
            if api_id != "":
                execute_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                update_api = ApiApi.objects.get(id=api_id)
                update_api.last_execute_time = execute_time
                update_api.api_real_result = result_data
                if int(http_code) == 200:
                    # 如果实际结果和数据库中存的期望结果一致，显示成功
                    if str(result_data).strip().lstrip() == str(update_api.api_expect_result).strip().lstrip():
                        is_success = 1
                        update_api.api_is_success = 1
                    else:
                        is_success = 0
                        update_api.api_is_success = 0
                else:
                    is_success = -1
                    update_api.api_is_success = -1
                update_api.save()
                heads["is_success"] = is_success
                heads["http_code"] = int(http_code)
        except Exception as ex:
            error_code = 110000
            heads["exception"] = str(ex)

    heads["code"] = error_code
    heads["message"] = errorinfo.change_to_message(error_code)
    result["heads"] = heads
    return result


