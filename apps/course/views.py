from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator
from operation.models import CourseComment
from operation.models import UserFavorite, UserCourse
from .models import *
from django.db.models import Q
from utils.mixin_utils import LoginRequired


# Create your views here.

# 课程列表
class CourseListView(View):
    def get(self, request):
        head = 'course'
        all_course = Course.objects.all()
        hot_course = all_course.order_by('-students')[:3]
        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords)|
                                           Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))    # name__icontains:sql中的like语句
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page:每页显示的条目个数
        p = Paginator(all_course, request=request, per_page=9)

        courses = p.page(page)
        return render(request, 'course/course-list.html', {
            'courses': courses,
            'head': head,
            'hot_course': hot_course,
            # 'cc': cc,
        })


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        course.click_nums += 1
        course.save()
        tag = course.tag
        course_user = False

        course_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=1):
                course_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                org_fav = True
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        return render(request, 'course/course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'course_fav': course_fav,
            'org_fav': org_fav,
            'course_user': course_user,
        })


# 开始学习-课程章节信息
class CourseVideoView(LoginRequired, View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            course.students += 1
            course.save()
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_lesson = course.lesson_set.all()
        all_resource = course.courseresource_set.all()
        return render(request, 'course/course-video.html', {
            'course': course,
            'all_lesson': all_lesson,
            'all_resource': all_resource,
            'related_courses': related_courses,
        })


# 评论课程页面
class CommentCourseView(LoginRequired, View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        all_resource = course.courseresource_set.all()
        all_comments = course.coursecomment_set.all()
        return render(request, 'course/course-comment.html', {
            'course': course,
            'all_resource': all_resource,
            'all_comments': all_comments,
        })


# 添加评论
class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status": "fail", "msg": "用户未登陆"}', content_type='application/json')
        else:
            course_id = request.POST.get('course_id', 0)
            comment = request.POST.get('comments', '')
            if int(course_id) > 0 and comment:
                course_comment = CourseComment()
                course = Course.objects.get(pk=course_id)
                course_comment.course = course
                course_comment.user = request.user
                course_comment.comment = comment
                course_comment.save()
                return HttpResponse('{"status": "success", "msg": "评论成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "评论失败"}', content_type='application/json')
