from django.urls import path
from .views import *
app_name = 'course'
urlpatterns = (
    path('course_list/', CourseListView.as_view(), name='course_list'),
    path('course_detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    # 开始学习
    path('course_video/<int:course_id>/', CourseVideoView.as_view(), name='course_video'),
    # 评论界面
    path('course_video_comment/<int:course_id>/', CommentCourseView.as_view(), name='course_video_comment'),
    # 添加评论
    path('add_comment/', AddCommentsView.as_view(), name='add_comment'),

)
