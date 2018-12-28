# Author Caozy

import xadmin
from .models import CourseOrg, CityDict, Teacher


class CourseOrgAdmin(object):
    list_display = ['name', 'disc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'disc', 'click_nums', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'disc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']


class CityDictAdmin(object):
    list_display = ['name', 'disc', 'add_time']
    search_fields = ['name', 'disc']
    list_filter = ['name', 'disc', 'add_time']


class TeacherAdmin(object):
    list_display = ['name', 'work_years', 'work_company', 'work_prosition']
    search_fields = ['name', 'work_years', 'work_company', 'work_prosition']
    list_filter = ['name', 'work_years', 'work_company', 'work_prosition']


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
