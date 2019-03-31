# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your models here.
from datetime import datetime
from django.db import models
from django.db.models import FilePathField

from organizations.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    teacher = models.ForeignKey(Teacher, verbose_name='课程讲师', null=True, blank=True, on_delete=models.CASCADE)
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=20)
    learn_times = models.IntegerField(default=20, verbose_name='学习时长')
    student = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='点赞人数')
    category = models.CharField(default='后端开发', max_length=50, verbose_name='课程类别')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面')
    tag = models.CharField(default='', max_length=20, verbose_name='课程标签')
    click_name = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    FilePathField(path="/home/images", match="foo.*", recursive=True)
    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_ZJ_nums(self):
        #获取章节总数
        return self.lesson_set.all().count()

    def get_learn_user(self):
        return self.usercourse_set.all()[:5]

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
