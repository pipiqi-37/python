from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import F

from unitle import contents


class User(AbstractUser):
    """ 用户基础信息表 """
    # username = models.CharField("用户名", max_length=64)
    # password = models.CharField("密码", max_length=255)
    avatar = models.ImageField("用户头像", upload_to="avatar", null=True, blank=True)
    integral = models.IntegerField("用户积分", default=0)
    level = models.SmallIntegerField("用户级别", default=0)

    class Meta:
        db_table = "accounts_user"
        verbose_name = "用户"
        verbose_name_plural = "用户"

    @property
    def default_addr(self):
        # 等同  UserAddress.objects.filter(user=user, is_valid=True)
        user_list = self.user_address.filter(is_valid=True)
        addr = None
        # 1 先判断用户是否有默认地址
        # 2 没有默认地址  默认返回第一个地址
        try:
            addr = user_list.filter(is_default=True)[0]
        except IndexError:
            try:
                addr = user_list[0]
            except IndexError:
                pass
        return addr

    def integral_account(self, types, count):
        # 0为扣除  1为充值
        if types == 1:
            self.integral = F('integral') + abs(count)
        else:
            self.integral = F('integral') - abs(count)
        self.save()
        self.refresh_from_db()


class UserProfile(models.Model):
    """ 用户的详细信息 """
    user = models.OneToOneField(User)
    real_name = models.CharField("真实姓名", max_length=64)
    email = models.EmailField("电子邮箱", max_length=128, null=True, blank=True)
    is_email_valid = models.BooleanField("电子邮箱是否验证", default=False)
    phone_num = models.CharField("电话号码", max_length=20, null=True, blank=True)
    is_phone_valid = models.BooleanField("电话号码是否验证", default=False)
    sex = models.SmallIntegerField("性别", default=1, choices=contents.SEX_CHOICES)
    age = models.SmallIntegerField("年龄", default=0)

    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    updated_time = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        db_table = "accounts_user_profile"
        verbose_name = "用户详细信息"
        verbose_name_plural = "用户详细信息"


class UserAddress(models.Model):
    """ 用户的地址信息 """
    user = models.ForeignKey(User, related_name="user_address")
    province = models.CharField("省", max_length=32)
    city = models.CharField("市", max_length=32)
    area = models.CharField("区", max_length=32)
    town = models.CharField("街道", max_length=32, null=True, blank=True)

    address = models.CharField("详细地址", max_length=64)
    username = models.CharField("收件人", max_length=16)
    phone = models.CharField("收件人电话", max_length=32)

    is_default = models.BooleanField("是否为默认地址", default=False)
    is_valid = models.BooleanField("是否有效", default=True)

    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    updated_time = models.DateTimeField("修改时间", auto_now=True)
    
    class Meta:
        db_table = "accounts_user_address"
        ordering = ["is_default", "-updated_time"]
        verbose_name = "用户地址"
        verbose_name_plural = "用户地址"

    def get_phone(self):
        """ 格式化手机 """
        return self.phone[:3] + "****" + self.phone[6:]

    def get_addr(self):
        """ 格式化省市区 """
        return "{self.province} {self.city} {self.area}".format(self=self)


class LoginRecord(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField("登录的账号", max_length=32)
    ip = models.CharField("IP", max_length=64)
    address = models.CharField("地址", max_length=32, null=True, blank=True)
    source = models.CharField("登录来源", max_length=32)

    created_time = models.DateTimeField("登录时间")

    class Meta:
        db_table = "accounts_login_record"