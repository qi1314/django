# _*_ coding:utf-8 _*_
import xadmin

from .models import *


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times'
        , 'student', 'fav_nums', 'image', 'click_name', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times'
        , 'student', 'fav_nums', 'image', 'click_name']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times'
        , 'student', 'fav_nums', 'image', 'click_name', 'add_time']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)