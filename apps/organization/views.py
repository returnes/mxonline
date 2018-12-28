from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict, Teacher
from operation.models import UserFavorite
from operation.models import UserAsk
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from django.db.models import Q
from courses.models import Course


# Create your views here.

class OrgView(View):

    def get(self, request):
        course_org = CourseOrg.objects.all()
        city_dict = CityDict.objects.all()
        search_keywords=request.GET.get('keywords','')
        if search_keywords:
            course_org=course_org.filter(Q(name__icontains=search_keywords)|Q(disc__icontains=search_keywords))
        city_id = request.GET.get('city', '')
        hot_org = CourseOrg.objects.order_by('-click_nums')[:3]
        # 筛选机构类型
        category = request.GET.get('ct', '')
        if category:
            course_org = course_org.filter(category=category)
        # 筛选出城市
        if city_id:
            course_org = course_org.filter(city_id=int(city_id))
        org_counts = course_org.count()

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                course_org.order_by('-study_nums')
            elif sort == 'courses':
                course_org.order_by('-course_nums')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(course_org, 5, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'course_org': orgs,
            'city_dict': city_dict,
            'org_counts': org_counts,
            'city_id': city_id,
            'category': category,
            'hot_org': hot_org,
            'sort': sort,
        })


class UserAskView(View):
    '''post提交，无需get'''

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # form 校验后可直接用一下方法提交到数据库，commit保存
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:  # 通知浏览器类型为json
            return HttpResponse('{"status":"fail", "msg":"输入错误"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums+=1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            if int(fav_type)==1:
                course=Course.objects.get(id=int(fav_id))
                if course.fav_nums<0:
                    course.fav_nums=1
                course.fav_nums-=1
                course.save()
            elif int(fav_type)==2:
                course_org=CourseOrg.objects.get(id=int(fav_id))
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 1
                course_org.fav_nums-=1
                course_org.save()
            elif int(fav_type)==3:
                teacher=Teacher.objects.get(id=int(fav_id))
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 1
                teacher.fav_nums-=1
                teacher.save()

            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teacher_count = all_teachers.count()
        search_keywords=request.GET.get('keywords','')
        if search_keywords:
            all_teachers=all_teachers.filter(Q(name__icontains=search_keywords)|Q(point__icontains=search_keywords))
        sort = request.GET.get('sort', '')
        if sort:
            all_teachers = all_teachers.order_by('-click_nums')
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sort': sort,
            'sorted_teachers': sorted_teachers,
            'teacher_count': teacher_count,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums+=1
        teacher.save()
        all_courses=teacher.course_set.all()
        # 本机构所有讲师
        org_id=teacher.org_id
        course_org=CourseOrg.objects.get(id=org_id)
        all_teacher=course_org.get_teachers().order_by('-fav_nums')
        has_fav_org = False
        has_fav_teacher = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'has_fav_org':has_fav_org,
            'has_fav_teacher':has_fav_teacher,
        })
