# -*- coding:utf-8 -*-

from django.db import models
from datetime import datetime
from organization.models import CourseOrg,Teacher


# Create your models here.
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, null=True, blank=True, verbose_name=u'课程机构')
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    category = models.CharField(max_length=200, default=u'后端开发', verbose_name=u'课程类别')
    is_banner=models.BooleanField(default=False,verbose_name=u'是否轮播')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=20, verbose_name=u'课程级别')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default='1', verbose_name=u'教师')
    course_note = models.CharField(max_length=300, default='',verbose_name=u'课程须知')
    teacher_note = models.TextField(default='',verbose_name=u'教师提示')
    learn_time = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面图片')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击量')
    tag = models.CharField(max_length=10, verbose_name=u'课程推荐', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_user(self):
        return self.usercourse_set.all()[:5]

    def get_learn_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程信息')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    learn_time = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    url = models.CharField(max_length=50, default='', verbose_name=u'资源链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
