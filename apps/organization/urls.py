from django.urls import path, re_path
from .views import *

app_name = 'organization'
urlpatterns = [
    # 课程机构url
    path('list/', OrgListView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    path('org_home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),
    path('org_course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),
    path('org_desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    path('org_teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),
    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name='add_fav'),
    # 讲师列表
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),

    path('teacher/detail/<int:teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),
    # 分享
    path('share/message/', SendShareEmailView.as_view(), name='share'),
]

