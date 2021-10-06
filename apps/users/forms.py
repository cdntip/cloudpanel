from django import forms
from django.contrib.auth.models import User

# 登录
class Login(forms.Form):
    username = forms.CharField(max_length=32, min_length=3, error_messages={'required': '账号不能为空', 'max_length': '账号最大长度为32位', 'min_length': '账号最小长度为4位'})
    password = forms.CharField(max_length=32, min_length=3, error_messages={'required': '密码不能为空', 'max_length': '密码最大长度为32位', 'min_length': '密码最小长度为4位'})
    code = forms.CharField(required=False, max_length=4, error_messages={'required': '验证码错误', 'max_length': '验证码错误'})

    # 判断账号是否存在
    def clean_username(self):
        username = self.cleaned_data.get('username').strip().lower()
        user_info = User.objects.filter(username=username).first()
        if not user_info:
            raise forms.ValidationError(message='该 %s 用户不存在' % username)
        self.cleaned_data.update({
            'user_info': user_info
        })
        return username

    # 处理密码
    def clean_password(self):
        password = self.cleaned_data.get('password').strip()
        return password
