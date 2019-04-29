"""MxOnline URL Configuration

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
# from django.contrib import admin
from django.urls import path, include, re_path
import xadmin
from django.views.static import serve
from users.views import ActiveUserView, IndexView
from MxOnline.settings import MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    # 用户url
    path('users/', include('users.urls', namespace='users')),
    # 用户激活
    re_path(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    # 图片验证码
    path('captcha/', include('captcha.urls')),
    # 课程机构
    path('org/', include('organization.urls', namespace='organization')),
    # 课程url
    path('course/', include('course.urls', namespace='course')),
    # 配置上传文件处理函数
    re_path(r'media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    # 富文本url
    re_path(r'^mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 全局404
handler404 = 'users.views.page_not_found'
# 全局500
handler500 = 'users.views.page_error'

