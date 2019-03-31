# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import UserInfoView, ImageUpload, UpdatePwdView, SendEmailView, UpdateEmailView, Col_courseView, Fav_org, Fav_teacher, Fav_Course

urlpatterns = [
    #用户信息
    url(r'^info/', UserInfoView.as_view(), name='info'),

    #用户头像上传
    url(r'^image/upload/', ImageUpload.as_view(), name='image_upload'),

    #更新用户密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    #发送邮箱验证码
    url(r'^send_email/$', SendEmailView.as_view(), name='send_email'),

    #更新邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    #我的收藏课程
    url(r'^col_course/$', Col_courseView.as_view(), name='col_course'),

    #我的收藏机构
    url(r'^fav_org/$', Fav_org.as_view(), name='fav_org'),

    #收藏讲师
    url(r'^fav_teacher/$', Fav_teacher.as_view(), name='fav_teacher'),

    #收藏课程
    url(r'^fav_course/$', Fav_Course.as_view(), name='fav_course'),

]