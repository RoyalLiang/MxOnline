# coding:utf-8
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=(('male', "男"), ('female', "女")), default="", max_length=6)
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='user/%Y/%m', default=u'image/default.png', max_length=128)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=24, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(verbose_name='验证类型', choices=(('register', "注册"), ('forget', "找回密码"),
                                                               ('update', "修改邮箱")), max_length=10)
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class Banner(models.Model):  # 首页轮播图
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to='banner/%Y-%m-%d', verbose_name="轮播图")
    url = models.URLField(max_length=256, verbose_name="访问地址", null=True, blank=True)
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
