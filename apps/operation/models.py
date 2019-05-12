from django.db import models
from datetime import datetime
from users.models import UserProfile
from course.models import Course
from organization.models import CourseOrg

# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=64, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name


# 课程评论
class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


# 用户收藏
class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1, "课程"), (2, "课程机构"), (3, "讲师")), default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=256, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    # def save(self, *args, **kwargs):
    #     """
    #     将新增加的课程课程学习人数添加到课程机构
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     self.course.course_org.students_nums += 1
    #     # 调用父类的 save 方法将数据保存到数据库中
    #     super(UserCourse, self).save(*args, **kwargs)
