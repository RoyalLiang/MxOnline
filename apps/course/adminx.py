from .models import *
from organization.models import CourseOrg
import xadmin


class CourseCategoryAdmin:
    list_display = ['name']


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'course_org', 'desc', 'degree', 'learn_time', 'students',
                    'fav_nums', 'image', 'click_nums', 'add_time']

    search_fields = ['name', 'desc', 'detail', 'degree', 'students',
                     'fav_nums', 'image', 'click_nums']

    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students',
                   'fav_nums', 'image', 'click_nums', 'add_time']

    exclude = ['fav_nums', 'click_nums', 'students']

    # 页面嵌套
    inlines = [LessonInline]
    # 列表页字段的直接修改
    # editable = ['degree']

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


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']

    search_fields = ['lesson', 'name']

    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']

    search_fields = ['course', 'name', 'download']

    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(CourseCategory, CourseCategoryAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
