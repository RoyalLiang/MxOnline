from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from .models import *
from .forms import *
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from utils.send_email import send_share_email

# Create your views here.


class OrgListView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_cities = CityDict.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
                                       Q(desc__icontains=search_keywords))  # name__icontains:sql中的like语句
        # 筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students_nums')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        org_number = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page:每页显示的条目个数
        p = Paginator(all_orgs, request=request, per_page=5)

        orgs = p.page(page)
        return render(request, 'org/org-list.html', {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_number': org_number,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,

        })


# 用户咨询
class AddUserAskView(View):
    def get(self, request):
        user_ask_form = UserAskForm(request.GET)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)
            return HttpResponse(json.dumps({'status': 'success'}))

        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': user_ask_form.errors}))

    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():

            user_ask = user_ask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')

        else:
            return HttpResponse('{"status": "fail", "msg": "留言失败"}', content_type='application/json')


# 机构详情页
class OrgHomeView(View):
    def get(self, request, org_id):
        orgleft = 'home'
        org_home = CourseOrg.objects.get(pk=org_id)
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_home.id), fav_type=2):
                has_fav = True
        # all_course = org_home.org_course.all()[:4]
        all_course = org_home.course_set.all()
        all_teacher = org_home.teacher_set.all()[:3]

        return render(request, 'org/org-detail-homepage.html', {
            'org_home': org_home,
            'all_course': all_course,
            'all_teacher': all_teacher,
            'orgleft': orgleft,
            'has_fav': has_fav,
        })


# 机构课程页
class OrgCourseView(View):
    def get(self, request, org_id):
        orgleft = 'course'
        org_home = CourseOrg.objects.get(pk=org_id)
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_home.id), fav_type=2):
                has_fav = True
        org_course = org_home.course_set.all()

        return render(request, 'org/org-detail-course.html', {
            'org_course': org_course,
            'org_home': org_home,
            'orgleft': orgleft,
            'has_fav': has_fav,
        })


# 机构介绍页
class OrgDescView(View):
    def get(self, request, org_id):
        orgleft = 'desc'
        org_home = CourseOrg.objects.get(pk=org_id)
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_home.id), fav_type=2):
                has_fav = True
        org_desc = org_home.desc
        return render(request, 'org/org-detail-desc.html', {
            'org_desc': org_desc,
            'org_home': org_home,
            'orgleft': str(orgleft),
            'has_fav': has_fav,
        })


# 机构教师页
class OrgTeacherView(View):
    def get(self, request, org_id):
        orgleft = 'teacher'
        org_home = CourseOrg.objects.get(pk=org_id)
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_home.id), fav_type=2):
                has_fav = True
        org_teacher = org_home.teacher_set.all()
        return render(request, 'org/org-detail-teachers.html', {
            'org_teacher': org_teacher,
            'org_home': org_home,
            'orgleft': orgleft,
            'has_fav': has_fav,
        })


# 用户收藏
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        # 判断用户是否登陆
        users = request.user.is_authenticated
        # users = int(users)
        if users:
            exit_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            # 如果记录存在，则删除记录
            if exit_record:
                exit_record.delete()
                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(pk=fav_id)
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(pk=fav_id)
                    org.fav_nums -= 1
                    if org.fav_nums < 0:
                        org.fav_nums = 0
                    org.save()
                elif int(fav_type) == 1:
                    course = Course.objects.get(pk=fav_id)
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')

            else:
                user_fav = UserFavorite()
                if int(fav_id) > 0 and int(fav_type) > 0:
                    if int(fav_type) == 3:
                        teacher = Teacher.objects.get(pk=fav_id)
                        teacher.fav_nums += 1
                        teacher.save()
                    elif int(fav_type) == 2:
                        org = CourseOrg.objects.get(pk=fav_id)
                        org.fav_nums += 1
                        org.save()
                    elif int(fav_type) == 1:
                        course = Course.objects.get(pk=fav_id)
                        course.fav_nums += 1
                        course.save()
                    user_fav.user_id = request.user.id
                    user_fav.fav_type = fav_type
                    user_fav.fav_id = fav_id
                    user_fav.save()
                    return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status": "fail", "msg": "收藏失败"}', content_type='application/json')

        else:
            return HttpResponse('{"status": "fail", "msg": "用户未登陆"}', content_type='application/json')


class TeacherListView(View):
    """
    讲师列表
    """
    def get(self, request):
        sort = request.GET.get('sort', '')
        all_teacher = Teacher.objects.all()
        teacher_num = all_teacher.count()
        hot_teacher = all_teacher.order_by('-click_nums')[:3]
        if sort == 'hot':
            all_teacher = all_teacher.order_by('-fav_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page:每页显示的条目个数
        p = Paginator(all_teacher, request=request, per_page=5)

        all_teacher = p.page(page)

        return render(request, 'teacher/teachers-list.html', {
            'all_teacher': all_teacher,
            'teacher_num': teacher_num,
            'hot_teacher': hot_teacher,
            'sort': sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        teacher_course = teacher.course_set.all()
        has_fav = False
        org_has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.id), fav_type=3):
                has_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org.id), fav_type=2):
                org_has_fav = True
        sort_teacher = Teacher.objects.all().order_by('-fav_nums')[:3]
        return render(request, 'teacher/teacher-detail.html', {
            'teacher': teacher,
            'teacher_course': teacher_course,
            'sort_teacher': sort_teacher,
            'has_fav': has_fav,
            'org_has_fav': org_has_fav,
        })


class SendShareEmailView(View):
    def post(self, request):
        info = request.POST.get('info', '')
        teacher = Teacher.objects.get(pk=int(info))
        send_share_email(teacher.name, teacher.work_years)
        return HttpResponse('{"status": "success", "msg": "已分享"}', content_type='application/json')

