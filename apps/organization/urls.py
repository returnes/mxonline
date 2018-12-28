# Author Caozy
from django.conf.urls import url, include
from organization.views import OrgView, UserAskView, OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView,TeacherListView,TeacherDetailView

urlpatterns = [
    # 机构模板继承
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^user_ask/$', UserAskView.as_view(), name='user_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    # 授课教师
    url(r'^teacher/list/$', TeacherListView.as_view(), name='org_teacher_list'),
    # 讲师详情页
    url(r'^teachers_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='org_teacher_detail'),
]
app_name = 'organization'
