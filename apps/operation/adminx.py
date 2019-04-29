from .models import *
import xadmin


class UserAskAdmin(object):
    pass


class CourseCommentAdmin(object):
    pass


class UserFavoriteAdmin(object):
    pass


class UserCourseAdmin(object):
    pass


class UserMessageAdmin(object):
    pass


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
