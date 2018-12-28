from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from .models import Course, CourseResource,Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        search_keywords=request.GET.get('keywords','')
        if search_keywords:
            all_courses=all_courses.filter(Q(name__icontains=search_keywords)|Q(detail__icontains=search_keywords)|Q(desc__icontains=search_keywords))
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses = all_courses.order_by('-students')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            tag_courses = Course.objects.filter(tag=tag)[:1]
        else:
            tag_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'tag_courses': tag_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,

        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students+=1
        course.save()

        # 将用户和课程关联
        users_course = UserCourse.objects.filter(user=request.user, course=course)
        if not users_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        users_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in users_course]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        all_course_ids = [user_course.course.id for user_course in all_user_courses]
        ralate_courses = Course.objects.filter(id__in=all_course_ids).order_by('-students')
        lessons = course.get_learn_lesson()
        course_sourses = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'lessons': lessons,
            'course_sourses': course_sourses,
            'ralate_courses': ralate_courses,

        })


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        lessons = course.get_learn_lesson()
        course_sourses = CourseResource.objects.filter(course=course)
        lesson_comments = CourseComments.objects.filter(course=course)

        users_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in users_course]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        all_course_ids = [user_course.course.id for user_course in all_user_courses]
        ralate_courses = Course.objects.filter(id__in=all_course_ids).order_by('-students')
        return render(request, 'course-comment.html', {
            'course': course,
            'lessons': lessons,
            'course_sourses': course_sourses,
            'lesson_comments': lesson_comments,
            'ralate_courses': ralate_courses,
        })


class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', '')
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comments = CourseComments()
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论不能为空"}', content_type='application/json')


class CoursePlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course=video.lesson.course
        course.students += 1
        course.save()
        lessons = course.get_learn_lesson()
        course_sourses = CourseResource.objects.filter(course=course)
        # 将用户和课程关联
        users_course = UserCourse.objects.filter(user=request.user, course=course)
        if not users_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        users_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in users_course]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        all_course_ids = [user_course.course.id for user_course in all_user_courses]
        ralate_courses = Course.objects.filter(id__in=all_course_ids).order_by('-students')
        return render(request, 'course-play.html', {
            'course': course,
            'lessons': lessons,
            'course_sourses': course_sourses,
            'ralate_courses': ralate_courses,
            'video':video,

        })
