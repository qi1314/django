# _*_ coding:utf-8 _*_
import xadmin
from .models import UserProfile, EmailVerifyRecord, Banner
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class UserProfileAdmin(object):
    list_display = ['nick_name', 'birday', 'gender', 'address', 'mobile', 'image']
    search_fields = ['nick_name', 'birday', 'gender', 'address', 'mobile', 'image']
    list_filter = ['nick_name', 'birday', 'gender', 'address', 'mobile', 'image']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)