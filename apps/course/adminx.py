import os

from django.contrib import auth

from MxOnline import settings
from .models import *
from utils import auth

from organization.models import CourseOrg
import xadmin


class CourseCategoryAdmin:
    list_display = ['name']


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'course_org', 'degree', 'learn_time', 'students',
                    'fav_nums', 'click_nums', 'add_time']

    search_fields = ['name', 'degree', 'click_nums']

    list_filter = ['name', 'degree', 'add_time']

    exclude = ['fav_nums', 'click_nums', 'students']


    # 页面嵌套
    inlines = [LessonInline]
    # 列表页字段的直接修改
    editable = ['degree']

    # style_fields = {'detail': 'ueditor'}
    import_excel = True

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)

    def save_models(self):
        """
        获取机构课程数
        :return:
        """
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']

    search_fields = ['course', 'name']

    list_filter = ['course__name', 'name', 'add_time']
    relfield_style = 'fk-ajax'


class VideoAdmin(object):
    list_display = ['get_video_course', 'lesson', 'name', 'add_time']

    search_fields = ['lesson', 'name']

    list_filter = ['lesson', 'name', 'add_time']
    relfield_style = 'fk-ajax'

    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.save()
        video_url = os.path.join(settings.MEDIA_ROOT, str(obj.video))
        # linux设置视频文件权限
        os.system("chmod 777 %s" % video_url)
        obj.image = 'video_image/%s' % auth.get_video_pic(video_url)
        obj.save()



class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'add_time']

    search_fields = ['course', 'name']

    list_filter = ['course', 'name', 'add_time']


class CourseAnnouncementAdmin:
    list_display = ['course', 'text', 'add_time']

    search_fields = ['course']

    list_filter = ['course', 'add_time']


xadmin.site.register(CourseCategory, CourseCategoryAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseAnnouncement, CourseAnnouncementAdmin)
