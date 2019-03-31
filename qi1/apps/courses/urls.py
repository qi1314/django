# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from .views import CourseListView, CourseDetailView,CourseResourceView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^resource/(?P<course_id>\d+)$', CourseResourceView.as_view(), name='course_resource'),

]
