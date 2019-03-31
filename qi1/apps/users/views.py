# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from courses.models import Course
from operation.models import UserCourse, UserFavorite
from organizations.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, ImageUploadForm, UserUpdateForm
from utils.mixin_utils import LoginRequiredMixin
from .models import UserProfile, EmailVerifyRecord, Banner
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from  django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from django.core.urlresolvers import reverse
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
                return None


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))#重新定向到首页，而且不能使用渲染
                else:
                    return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})

            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})


class LogOutView(View):
    """
    用户登出重定向
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户名已经存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(email, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user =UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
#设置链接过期时间，即可提示用户链接已经过期
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form':modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserUpdateForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')



class ImageUpload(LoginRequiredMixin, View):
    """
    用户头像上传
    """
    def post(self, request):
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    更新用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            # 设置链接过期时间，即可提示用户链接已经过期
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email, 'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        exist_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')

        if exist_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class Col_courseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        course_list = []
        user_course = UserCourse.objects.filter(user=request.user)
        for courses in user_course:
            course = courses.course
            course_list.append(course)
        return render(request, 'usercenter-mycourse.html', {
            'course_list': course_list,
        })


class Fav_org(LoginRequiredMixin, View):
    """
    收藏机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2).order_by('-add_time')
        for org in fav_orgs:
            org_id = org.fav_id
            org1 = CourseOrg.objects.get(id=org_id)
            org_list.append(org1)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter()[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


class Fav_teacher(LoginRequiredMixin, View):
    """
    收藏讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3).order_by('-add_time')
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class Fav_Course(LoginRequiredMixin, View):
    """
    收藏课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1).order_by('-add_time')
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


def page_not_found(request):
    #全局处理404错误
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response