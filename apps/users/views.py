from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from .models import UserProfile, EmailVerifyRecord, Banner
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.send_email import send_register_email
from utils.mixin_utils import LoginRequired
from django.http import HttpResponse, HttpResponseRedirect
import json
from operation.models import UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from course.models import Course
from pure_pagination import PageNotAnInteger, Paginator



# Q：并集查询


# Create your views here.
# 使用户可以使用邮箱等登陆
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        link = 'index'
        courses = Course.objects.all()[:6]
        orgs = CourseOrg.objects.all()[:15]
        all_banner = Banner.objects.all().order_by('index')[:5]
        return render(request, 'index.html', {
            'link': link,
            'courses': courses,
            'orgs': orgs,
            'all_banner': all_banner,

        })


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                user_message = UserMessage()
                user_message.user = int(user.id)
                user_message.message = '欢迎注册慕学在线网。'
                user_message.save()
            from django.urls import reverse
            return HttpResponseRedirect(reverse('index'))
            # return render(request, 'active_success.html')
        else:
            pass


class OutLoginView(View):
    def get(self, request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse('index'))

    def post(self, request):
        pass


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # authenticate用来验证用户名和密码是否正确
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    from django.urls import reverse
                    return HttpResponseRedirect(reverse('index'))
                    # return render(request, 'index.html', {'user': user})
                else:
                    return render(request, 'user/login.html', {'msg': '用户未激活。'})
            else:
                return render(request, 'user/login.html', {'msg': '用户名或密码错误。'})
        else:
            return render(request, 'user/login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'user/register.html', {'msg': '该邮箱已注册'})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            # 加密密码
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(email, 'register')
            return render(request, 'user/login.html')
        else:
            return render(request, 'user/register.html', {'register_form': register_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'user/forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                send_register_email(email, 'forget')
                return render(request, 'user/login.html')
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'user/forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'user/password_reset.html', {'email': email})
        else:
            pass


class ResetView(View):
    def post(self, request):
        reset_form = ModifyPwdForm(request.POST)
        if reset_form.is_valid():
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 == password2:
                user = UserProfile.objects.get(email=email)
                if user:
                    user.password = make_password(password2)
                    user.save()
                    return render(request, 'user/reset_success.html')
                else:
                    return render(request, {'reset_form': reset_form})
            else:
                return render(request, {'msg': '密码不一致'})
        else:
            return render(request, {'reset_form': reset_form})


# 用户中心
class UserInfoView(LoginRequired, View):
    def get(self, request):
        user = request.user
        link = 'info'
        all_message = UserMessage.objects.filter(user=user.id, has_read=False)
        return render(request, 'user/usercenter-info.html', {
            'user': user,
            'link': link,
            'all_message': all_message,
        })

    def post(self, request):
        """
        修改用户信息
        """
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequired, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            # # 取出传过来的iamge
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            # return render(request, 'usercenter-info.html', {
            #     'user': user,
            # })
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(image_form.errors), content_type='application/json')


class ModifyPwdView(LoginRequired, View):
    """
    修改密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 == password2:
                request.user.password = make_password(password1)
                user_message = UserMessage()
                user_message.user = int(request.user.id)
                user_message.message = '尊敬的用户，您的密码已修改。'
                user_message.save()
                request.user.save()
                return HttpResponse('{"status": "success"}', content_type='application/json')

            else:
                return HttpResponse('{"status": "fail", "msg": "两次密码不一致"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailView(LoginRequired, View):
    """
    修改用户邮箱，发送验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'update')
        return HttpResponse('{"status": "success"}', content_type='application/json')


class ModifyEmailView(View):
    """
    修改用户邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if EmailVerifyRecord.objects.filter(code=code, email=email, send_type='update'):
            request.user.email = email
            user_message = UserMessage()
            user_message.user = int(request.user.id)
            user_message.message = '尊敬的用户，您的绑定邮箱已修改。'
            user_message.save()
            request.user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码错误"}', content_type='application/json')


# 我的课程
class UserCourseView(LoginRequired, View):
    def get(self, request):
        user = request.user
        link = 'course'
        all_message = UserMessage.objects.filter(user=user.id, has_read=False)
        return render(request, 'user/usercenter-mycourse.html', {
            'user': user,
            'link': link,
            'all_message': all_message,

        })


# 我的收藏
# class UserFavView(LoginRequired, View):
#     def get(self, request, fav_type):
#         user = request.user
#         link = 'fav'
#         if fav_type == 'org':
#             user_fav = UserFavorite.objects.filter(user=user, fav_type=2)
#             user_fav_org_ids = [user_org.fav_id for user_org in user_fav]
#             user_fav_org = CourseOrg.objects.filter(id__in=user_fav_org_ids)
#             return render(request, 'usercenter-fav-org.html', {
#                 'user': user,
#                 'link': link,
#                 'fav_type': fav_type,
#                 'user_fav_org': user_fav_org,
#             })
#         elif fav_type == 'course':
#             user_fav = UserFavorite.objects.filter(user=user, fav_type=1)
#
#             user_fav_course_ids = [user_course.fav_id for user_course in user_fav]
#             user_fav_course = Course.objects.filter(id__in=user_fav_course_ids)
#             return render(request, 'usercenter-fav-course.html', {
#                 'user': user,
#                 'link': link,
#                 'fav_type': fav_type,
#                 'user_fav_course': user_fav_course,
#
#             })
#         elif fav_type == 'teacher':
#             user_fav = UserFavorite.objects.filter(user=user, fav_type=3)
#             user_fav_teacher_ids = [user_teacher.fav_id for user_teacher in user_fav]
#             user_fav_teacher = Teacher.objects.filter(id__in=user_fav_teacher_ids)
#             return render(request, 'usercenter-fav-teacher.html', {
#                 'user': user,
#                 'link': link,
#                 'fav_type': fav_type,
#                 'user_fav_teacher': user_fav_teacher,
#
#             })
#         else:
#             pass


class UserFavOrgView(View):
    def get(self, request):
        user = request.user
        link = 'fav'
        fav_type = 'org'
        all_message = UserMessage.objects.filter(user=user.id, has_read=False)
        user_fav = UserFavorite.objects.filter(user=user, fav_type=2)
        user_fav_org_ids = [user_org.fav_id for user_org in user_fav]
        user_fav_org = CourseOrg.objects.filter(id__in=user_fav_org_ids)
        return render(request, 'user/usercenter-fav-org.html', {
            'user': user,
            'link': link,
            'user_fav_org': user_fav_org,
            'fav_type': fav_type,
            'all_message': all_message,

        })


class UserFavTeacherView(View):
    def get(self, request):
        user = request.user
        link = 'fav'
        fav_type = 'teacher'
        all_message = UserMessage.objects.filter(user=user.id, has_read=False)
        user_fav = UserFavorite.objects.filter(user=user, fav_type=3)
        user_fav_teacher_ids = [user_teacher.fav_id for user_teacher in user_fav]
        user_fav_teacher = Teacher.objects.filter(id__in=user_fav_teacher_ids)
        return render(request, 'user/usercenter-fav-teacher.html', {
            'user': user,
            'link': link,
            'user_fav_teacher': user_fav_teacher,
            'fav_type': fav_type,
            'all_message': all_message,

        })


class UserFavCourseView(View):
    def get(self, request):
        user = request.user
        link = 'fav'
        fav_type = 'course'
        all_message = UserMessage.objects.filter(user=user.id, has_read=False)
        user_fav = UserFavorite.objects.filter(user=user, fav_type=1)
        user_fav_course_ids = [user_course.fav_id for user_course in user_fav]
        user_fav_course = Course.objects.filter(id__in=user_fav_course_ids)
        return render(request, 'user/usercenter-fav-course.html', {
            'user': user,
            'link': link,
            'user_fav_course': user_fav_course,
            'fav_type': fav_type,
            'all_message': all_message

        })


class UserMessageView(View):
    def get(self, request):
        user = request.user
        link = 'message'
        all_message = UserMessage.objects.filter(user=user.id, has_read=False)
        my_message = UserMessage.objects.filter(user=user.id).order_by('-add_time')
        my_message.update(
            has_read=True
        )
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page:每页显示的条目个数
        p = Paginator(my_message, request=request, per_page=9)

        my_message = p.page(page)
        return render(request, 'user/usercenter-message.html', {
            'link': link,
            'user': user,
            'all_message': all_message,
            'my_message': my_message,
        })


def page_not_found(request, exception):
    """
    全局404函数
    :param request:
    :return:
    """
    from django.shortcuts import render_to_response
    response = render_to_response('error_page/404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    """
    全局500函数
    :param request:
    :return:
    """
    from django.shortcuts import render_to_response
    response = render_to_response('error_page/500.html', {})
    response.status_code = 500
    return response



