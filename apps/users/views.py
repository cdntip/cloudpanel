from django.http import JsonResponse
from django.core.cache import cache

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.users import forms

# Create your views here.
import time

from libs.utils import md5
# 判断是否登录
def is_token(func):
    def inner(request, *args, **kwargs):
        token = request.META.get('HTTP_X_TOKEN', False)
        if not token:
            return JsonResponse({'code': 50008, 'message': '登录会话失效，请重新的登录'})

        user = cache.get(token, False)
        if not user or not user.is_active or not user.is_superuser:
            return JsonResponse({'code': 50008, 'message': '登录会话失效，请重新的登录'})
        request.user = user
        return func(request, *args, **kwargs)
    return inner


# 登录
def Login(request):
    if request.method == "POST":
        input_data = forms.Login(request.POST)
        if input_data.is_valid():
            data = input_data.clean()
            user_info = data.get('user_info')
            username = data.get('username')
            password = data.get('password')

            if not user_info.is_active:
                return JsonResponse({'code': 20002, 'message': '该用户禁止登录'})

            user = authenticate(username=username, password=password)

            if not user: return JsonResponse({'code': 20002, 'message': '登录密码错误'})

            token = md5("%s%s" %(user.username, time.time())).upper()
            cache.set(token, user, 172800)
            res_data = {'code': 20000,  'message': '登录成功', 'data': {'token': token}}
            return JsonResponse(res_data)
        return JsonResponse({'code': 20001, 'message': '登录失败', 'error_data': input_data.errors})

# 获取用户信息
@is_token
def Info(request):
    userinfo = User.objects.filter(username=request.user.username).first()
    if not userinfo:
        return JsonResponse({'code': 50008, 'message': '用户信息不存在，请重新登录'})
    data = {
        'avatar': 'https://t1.picb.cc/uploads/2021/10/05/wXMX1y.th.jpg',
        'name': userinfo.username,
        'username': userinfo.username,
        'create_time': userinfo.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        'roles': ['user']
    }
    if userinfo.is_superuser:
        # 管理员
        data.update({'roles': ['admin'], 'introduction': '.'})

    return JsonResponse({'code': 20000, 'message': '获取成功', 'data': data})

# 退出
def Logout(request):
    cache.set(request.token, '', 0)
    return JsonResponse({'code': 20000, 'data': 'success'})