# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render
from .models import Course
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserCourse, UserFavorite
from .models import CourseResource
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        sort = request.GET.get('sort', '')
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_courses = all_courses.filter(Q(name__icontains=search_keyword)|Q(desc__icontains=search_keyword)|Q(detail__contains=search_keyword))

        hot_courses = all_courses.order_by('-click_name')[:3]
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_name')
            elif sort == 'student':
                all_courses = all_courses.order_by('-student')

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page =1
        p = Paginator(all_courses, 3, request=request)
        all_courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': all_courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #增加课程点击数
        course.click_name +=1
        course.save()
        #设置标签，来确定课程相关
        tag = course.tag
        #检查是否收藏该课程
        course_has_fav = False
        #检查是否收藏该机构
        org_has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                course_has_fav = True
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                org_has_fav = True
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:2]
        else:
            relate_course = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'course_has_fav':course_has_fav,
            'org_has_fav':org_has_fav,
        })


#确保是登录状态
class CourseResourceView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course =Course.objects.get(id=int(course_id))
        #查询用户是否已经关联了该课程
        user_cou = UserCourse.objects.filter(user=request.user, course=course)
        if not user_cou:
            user_cou1 =UserCourse(user=request.user, course=course)
            course.student+=1
            user_cou1.save()
            course.save()
        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user_co.user.id for user_co in user_course]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_name')[:3]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })
