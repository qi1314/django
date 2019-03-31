# -*- coding: utf-8 -*-
from django import forms

from operation.models import UserAsk
import re

# class UserAsk(forms.Form):#from表单注册限制
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


class UserAskForm(forms.ModelForm):#modelForm继承models

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile =self.cleaned_data['mobile']#获取数据
        regex_mobile = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}'
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')