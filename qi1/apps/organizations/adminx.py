# _*_ coding:utf-8 _*_

import xadmin

from .models import *


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    list_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_num', 'image',
                    'address', 'city', 'add_time']
    list_fields = ['name', 'desc', 'click_nums', 'fav_num', 'image',
                   'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_num', 'image',
                   'address', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company',
                    'work_position', 'points', 'click_name', 'fav_nums',
                    'add_time']
    list_fields = ['org', 'name', 'work_year', 'work_company',
                   'work_position', 'points', 'click_name', 'fav_nums']
    list_filter = ['org', 'name', 'work_year', 'work_company',
                   'work_position', 'points', 'click_name', 'fav_nums',
                   'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)