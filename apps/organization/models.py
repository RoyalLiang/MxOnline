from django.db import models
from datetime import datetime
# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=64, verbose_name="城市名")
    desc = models.CharField(max_length=256, verbose_name="城市描述", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    CHOICE = (('pxjg', '培训机构'), ('gx', '高校'), ('gr', '网课'))
    name = models.CharField(max_length=64, verbose_name="机构名")
    desc = models.CharField(max_length=256, verbose_name="机构描述", null=True, blank=True)
    category = models.CharField(default='pxjg', max_length=16, choices=CHOICE, verbose_name='机构类别')
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to='organization/org/%Y-%m', verbose_name="logo")
    click_nums = models.IntegerField(default=0, verbose_name="浏览量")
    address = models.CharField(max_length=64, verbose_name="机构地址")
    students_nums = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="机构课程", null=True, blank=True)
    city = models.ForeignKey(CityDict, verbose_name="城市", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def increase_click_nums(self):
        self.click_nums += 1
        self.save(update_fields=['click_nums'])

    def increase_fav_nums(self):
        self.fav_nums += 1
        self.save(update_fields=['fav_nums'])

    def increase_students_nums(self):
        self.students_nums += 1
        self.save(update_fields=['students_nums'])


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限", null=True, blank=True)
    points = models.CharField(max_length=64, verbose_name="教学特点", null=True, blank=True)
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0, verbose_name="浏览量")
    image = models.ImageField(upload_to='organization/teacher/%Y-%m', verbose_name="头像",
                              default='', blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.org.name + ' ' + self.name

    def get_teacher_count(self):
        return self.objects.all().count()

    def increase_click_nums(self):
        self.click_nums += 1
        self.save(update_fields=['click_nums'])

    def increase_fav_nums(self):
        self.fav_nums += 1
        self.save(update_fields=['fav_nums'])

