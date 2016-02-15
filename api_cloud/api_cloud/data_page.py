# -*- coding:utf8 -*-
from django.core.paginator import Paginator


def data_page(request, data_object, pagesize, step=10):
    page = request.GET.get("page", 1)
    try:
        pagesize = int(pagesize)
        page = int(page)
    except:
        pagesize = 10
        page = 1
    paginator = Paginator(data_object, pagesize)
    try:
        data_info = paginator.page(page)
    except:
        data_info = ""
    #根据参数配置导航显示范围
    if page >= step:
        page_range = paginator.page_range[step-1: paginator.num_pages]
    else:
        page_range = paginator.page_range[0:step]
    return data_info, page_range, paginator
