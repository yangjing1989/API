# -*- coding:utf8 -*-
def change_to_message(code_num):
    message = ""
    if code_num == 100000:
        message = "用户名或密码错误"
    elif code_num == 100001:
        message = "Hosts 名称已存在"
    elif code_num == 100002:
        message = "Hosts 名称不能为空"
    elif code_num == 100003:
        message = "Hosts 不存在"
    elif code_num == 100013:
        message = "不能删除当前Hosts"
    elif code_num == 100004:
        message = "接口名称不能为空"
    elif code_num == 100005:
        message = "接口名称已存在"
    elif code_num == 100006:
        message = "接口不存在"
    elif code_num == 100007:
        message = "接口地址不能为空"
    elif code_num == 100008:
        message = "接口域名不能为空"
    elif code_num == 100009:
        message = "域名不可达"
    elif code_num == 100010:
        message = "请先保存接口基本信息"
    elif code_num == 100011:
        message = "执行结果为空"
    elif code_num == 100012:
        message = "项目名称不能为空"
    elif code_num == 100013:
        message = "项目名称已存在"
    elif code_num == 100014:
        message = "项目不存在"
    elif code_num == 100015:
        message = "用户名不能为空"
    elif code_num == 100016:
        message = "用户姓名不能为空"
    elif code_num == 100017:
        message = "用户已存在"
    elif code_num == 100018:
        message = "用户不存在"
    elif code_num == 100019:
        message = "两次输入的密码不一致"
    elif code_num == 100020:
        message = "密码必须大于等于6位"
    elif code_num == 100021:
        message = "密码不能为空"
    elif code_num == 100022:
        message = "已有该权限"
    elif code_num == 100023:
        message = "旧密码错误"
    elif code_num == 100024:
        message = "项目下存在接口用例，无法删除"
    elif code_num == 100025:
        message = "不能删除所有管理员"
    elif code_num == 100026:
        message = "不能删除当前登录用户"
    elif code_num == 100027:
        message = "非创建者，不能删除此接口"
    elif code_num == 100028:
        message = "项目下存在子项目，无法删除"
    elif code_num == 110000:
        message = "异常"
    return message
