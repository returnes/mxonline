# -*- coding:utf-8 -*-
from django.db import models
from datetime import datetime


# Create your models here.

class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    disc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    category = models.CharField(max_length=20, verbose_name='培训类别',
                                choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')), default='pxjg')
    disc = models.TextField(verbose_name=u'机构描述')
    tag=models.CharField(max_length=20,default=u'全国知名',verbose_name=u'知名度')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击量')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    study_nums = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    image = models.ImageField(upload_to='organization/%Y/%m', verbose_name=u'封面图')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u'所在城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'机构信息'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def get_teachers(self):
        return self.teacher_set.all()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u'所属机构')
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    age = models.IntegerField(default=40, verbose_name=u'年龄')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_prosition = models.CharField(max_length=50, verbose_name=u'公司职位')
    point = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击量')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u'头像')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
