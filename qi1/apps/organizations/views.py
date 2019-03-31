# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.views.generic import View
from django.shortcuts import render

from courses.models import Course
from .models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .form import UserAskForm
from django.http import HttpResponse
from operation.models import UserFavorite
# Create your views here.


class OrgView(View):

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        city_id = request.GET.get('city', '')
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))

        #涮选城市
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        #刷选机构
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(catgory=category)
        sort = request.GET.get('sort', '')#排序分类
        if sort:
            if sort =='students':
                all_orgs = all_orgs.order_by('-student')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html',
                      {
                          'all_orgs': orgs,
                          'all_citys': all_citys,
                          'org_nums': org_nums,
                          'city_id': city_id,
                          'category': category,
                          'hot_orgs': hot_orgs,
                          'sort': sort,
                      })


class AddUserAskFormView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        all_courses = org.course_set.all()[:3]
        all_teachers = org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'org': org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        all_courses = org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'org': org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'org': org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        all_teachers = org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'org': org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    """
    用户收藏与取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():#用户没有登录
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        # hav_fav = False#检查是否收藏
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"fail", "msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user = request.user
                user_fav.fav_type = fav_type
                user_fav.fav_id = fav_id
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_name')
        hot_teachers = teachers.order_by('-click_name')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 3, request=request)
        teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'sort': sort,
            'hot_teachers': hot_teachers,
        })


class TeacherDetailView(View):

    def get(self, request, teacher_id):
        teachers = Teacher.objects.all()
        hot_teachers = teachers.order_by('-click_name')[:3]
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_name+=1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)
        T_has_fav = False
        Org_has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                T_has_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                Org_has_fav = True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'hot_teachers': hot_teachers,
            'T_has_fav': T_has_fav,
            'Org_has_fav': Org_has_fav,
        })







