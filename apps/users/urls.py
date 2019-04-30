from django.urls import path, re_path
from .views import *
app_name = 'users'
urlpatterns = (
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    # 忘记密码
    path('forget/', ForgetPwdView.as_view(), name='forget'),
    re_path(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name='user_reset'),
    path('reset/', ResetView.as_view(), name='reset_pwd'),
    # 登出
    path('logout/', OutLoginView.as_view(), name='logout'),
    # 用户信息
    path('user_info/', UserInfoView.as_view(), name='user_info'),
    # 用户头像
    path('user/image/', UploadImageView.as_view(), name='user-image'),
    # 用户密码修改
    path('update/pwd/', ModifyPwdView.as_view(), name='update-pwd'),
    # 用户邮箱修改，发送邮箱验证码
    path('sendemail_code/', SendEmailView.as_view(), name='sendemail_code'),
    # 用户邮箱修改
    path('update_email/', ModifyEmailView.as_view(), name='update_email'),
    # 修改用户信息
    # path('info/', UserInfoView.as_view(), name='info'),
    # 用户课程
    path('user_course/', UserCourseView.as_view(), name='user_course'),
    # 用户收藏(机构，教师，课程)
    # re_path(r'^user_fav/(?P<fav_type>.*)/$', UserFavView.as_view(), name='user_fav'),
    # 用户收藏机构
    path('user_fav/org/', UserFavOrgView.as_view(), name='user_fav_org'),
    # 教师
    path('user_fav/teacher/', UserFavTeacherView.as_view(), name='user_fav_teacher'),
    # 课程
    path('user_fav/course/', UserFavCourseView.as_view(), name='user_fav_course'),
    # 用户消息
    path('user_message/', UserMessageView.as_view(), name='user_message'),

)

