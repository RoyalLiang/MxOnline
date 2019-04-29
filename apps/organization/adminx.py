from .models import *
import xadmin


class CityDictAdmin(object):
    pass


class CourseOrgAdmin(object):
    list_display = ['name', 'fav_nums', 'click_nums', 'course_nums', 'students_nums', 'address']
    # 设置只读字段
    readonly_fields = ['add_time']
    # 设置字段不可见
    exclude = ['fav_nums', 'click_nums', 'course_nums', 'students_nums']
    # 设置外键指向该model时，使用ajax模式
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    relfield_style = 'fk-ajax'
    exclude = ['fav_nums', 'click_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
