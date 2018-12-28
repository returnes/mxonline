from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, ChangeImageForm, ChangeInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from users.models import Banner
import json


# Create your views here.

class CustomBackend(ModelBackend):
    '''自定义类重写authenticate，自定义后台验证方式'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    '''接收邮箱链接访问激活注册'''

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': "用户已经存在"})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, 'register')  # 邮箱验证

            return render(request, 'login.html', {'msg': '请邮箱中打开连接激活账号'})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                    # return render(request, "index.html", {'username': user_name, 'password': pass_word})
                else:
                    return render(request, 'login.html', {'msg': '用户名密码不匹配'})
            else:
                return render(request, 'login.html', {'msg': '用户名密码不匹配'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forgetform': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_seccess.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetform': forget_form, 'msg': '填写错误'})


class ResetView(View):
    '''接收邮箱链接访问激活注册'''

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': "两次输入的密码不一致"})
            user = UserProfile.objects.get(email=email)
            print(user.password)
            user.password = make_password(pwd2)
            print(user.password)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    个人中心用户信息
    """

    def get(self, request):
        current_page = 'info'
        return render(request, 'usercenter-info.html', {'current_page': current_page})

    def post(self, request):
        change_form = ChangeInfoForm(request.POST, instance=request.user)
        if change_form.is_valid():
            change_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(change_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    '''
    个人中心刚换头像
    '''

    def post(self, request):
        image_form = ChangeImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image=image_form.cleaned_data['image']
            # request.user.image=image
            # request.user.save()
            image_form.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:  # 通知浏览器类型为json
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    '''个人中心更新密码'''

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    '''发送修改邮箱验证码'''

    def get(self, request):
        email = request.GET.get('email', '')
        userprofile = UserProfile.objects.filter(email=email)
        if userprofile:
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, send_type='update')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''个人中心更新邮箱'''

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code')
        exists_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
        if exists_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'mycourse'
        all_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'all_courses': all_courses,
            'current_page': current_page
        })


class FavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav_org'
        org_list = []
        favorite_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for favorite_org in favorite_orgs:
            org_id = favorite_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {'org_list': org_list, 'current_page': current_page})


class FavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav_org'
        teacher_list = []
        favorite_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for favorite_teacher in favorite_teachers:
            teacher_id = favorite_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html',
                      {'teacher_list': teacher_list, 'current_page': current_page})


class FavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav_org'
        course_list = []
        favorite_teachers = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for favorite_teacher in favorite_teachers:
            course_id = favorite_teacher.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {'course_list': course_list, 'current_page': current_page})


class MessageView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'message'
        all_message = UserMessage.objects.filter(user=request.user.id)
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_message, 5, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {'all_message': messages, 'current_page': current_page})


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=False)[:3]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        })


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
