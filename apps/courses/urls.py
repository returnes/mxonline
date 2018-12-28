# Author Caozy
from django.conf.urls import url, include
from courses.views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentsView,CoursePlayView

urlpatterns = [
    # 机构模板继承
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/$', AddCommentsView.as_view(), name='add_comment'),

    url(r'^video/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name='video_play'),

]
app_name = 'course'
