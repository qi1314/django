# -*- coding: utf-8 -*-
# forms用来限制登录条件的选择

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):#登录限制
    #字段必须与form表单传过来的名称一致
    username = forms.CharField(required=True, min_length=5)
    password = forms.CharField(required=True)


class RegisterForm(forms.Form):#注册限制
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetForm(forms.Form):#忘记密码限制
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):#更改密码限制,表单中必须有这些字段，否则无效
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class ImageUploadForm(forms.ModelForm):
    #modelform
    class Meta:
        model = UserProfile
        fields = ['image']


class UserUpdateForm(forms.ModelForm):
    #modelform
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']
