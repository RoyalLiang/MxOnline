from django.db import models
from datetime import datetime
from organization.models import Teacher, CourseOrg
from users.models import UserProfile
from mdeditor.fields import MDTextField

# Create your models here.


class CourseCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name="课程类别名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='教授机构', null=True, blank=True, on_delete=models.CASCADE)
    course_teacher = models.ForeignKey(Teacher, verbose_name='教授讲师', null=True, blank=True, on_delete=models.CASCADE)
    course_category = models.ForeignKey(CourseCategory, verbose_name="课程类别", on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name="课程名")
    desc = models.CharField(max_length=256, verbose_name="课程描述")
    detail = MDTextField(verbose_name='课程详情')
    degree = models.CharField(verbose_name='难度', choices=(('cj', "初级"), ('zj', "中级"), ('gj', "高级")), max_length=32)
    learn_time = models.IntegerField(default=0, verbose_name="学习时长")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name="封面", blank=True)
    tag = models.CharField(default='', max_length=20, verbose_name="课程标签")
    click_nums = models.IntegerField(default=0, verbose_name="浏览量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson(self):
        return self.lesson_set.all().count()

    def get_course_user(self):
        return self.usercourse_set.all()[:5]

    def save(self, *args, **kwargs):
        """
        将新增加的课程添加到课程机构
        :param args: 
        :param kwargs: 
        :return: 
        """
        self.course_org.course_nums += 1
        # 调用父类的 save 方法将数据保存到数据库中
        super(Course, self).save(*args, **kwargs)
        
    def increase_click_nums(self):
        self.click_nums += 1
        self.save(update_fields=['click_nums'])
        
    def increase_fav_nums(self):
        self.fav_nums += 1
        self.save(update_fields=['fav_nums'])
        
    def increase_students_nums(self):
        self.students += 1
        self.save(update_fields=['students'])


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name="视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    url = models.CharField(max_length=128, verbose_name="访问地址", default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=32, verbose_name="名称")
    download = models.FileField(upload_to='course/resource/%X', verbose_name="资源")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
