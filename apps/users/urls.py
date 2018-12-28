# Author Caozy
from django.conf.urls import url, include
from users.views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView,MyCourseView,FavOrgView,FavTeacherView,FavCourseView,MessageView

urlpatterns = [
    # 机构模板继承
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    # 修改头像
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 获取修改邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='send_email_code'),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 我的收藏
    url(r'^fav_org/$', FavOrgView.as_view(), name='fav_org'),
    url(r'^fav_teacher/$', FavTeacherView.as_view(), name='fav_teacher'),
    url(r'^fav_course/$', FavCourseView.as_view(), name='fav_course'),
    # 我的消息
    url(r'^message/$', MessageView.as_view(), name='message'),

]
app_name = 'users'