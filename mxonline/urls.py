"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import url, include
import xadmin  # admin # admin123
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView
from organization.views import OrgView
from django.views.static import serve
from mxonline.settings import MEDIA_ROOT,STATIC_ROOT
from users.views import IndexView
from mxonline import settings

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^login/$', TemplateView.as_view(template_name='login.html'),name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # org模板继承
    url(r'^org/', include('organization.urls', namespace='org')),
    # course模板继承
    url(r'^course/', include('courses.urls', namespace='course')),
    # 配置文件上传的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # users模板继承
    url(r'^users/', include('users.urls', namespace='users')),

    url(r'^static/(?P<path>.*)$', serve,{'document_root': STATIC_ROOT}),

]

# 全局配置404/500页面
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
