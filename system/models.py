from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

# Create your models here.
from unitle import contents


class Slider(models.Model):
    """ 系统的轮播图 """
    name = models.CharField("名称", max_length=32)
    desc = models.CharField("描述", max_length=100, null=True, blank=True)
    types = models.SmallIntegerField("展示的位置",
                                     choices=contents.SLIDER_TYPES_CHOICES,
                                     default=contents.SLIDER_TYPES_INDEX)
    img = models.ImageField("图片", upload_to="slider")
    reorder = models.SmallIntegerField("排序", default=0, help_text="数字越大越靠前")
    start_time = models.DateTimeField("生效开始时间", null=True, blank=True)
    end_time = models.DateTimeField("生效结束时间", null=True, blank=True)
    target_url = models.CharField("图片跳转链接", max_length=255, null=True, blank=True)
    is_valid = models.BooleanField("是否删除", default=True)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    updated_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "system_slider"
        ordering = ["-reorder"]
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图"


class News(models.Model):
    types = models.SmallIntegerField("类型",
                                     choices=contents.NEWS_TYPES_CHOICES,
                                     default=contents.NEWS_TYPES_NEW)
    title = models.CharField("标题", max_length=255)
    content = models.TextField("内容")
    is_top = models.BooleanField("是否置顶", default=False)
    view_count = models.IntegerField("浏览次数", default=0)
    reorder = models.SmallIntegerField("排序", default=0, help_text="数字越大越靠前")
    start_time = models.DateTimeField("生效开始时间", null=True, blank=True)
    end_time = models.DateTimeField("生效结束时间", null=True, blank=True)
    is_valid = models.BooleanField("是否删除", default=True)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    updated_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "system_news"
        ordering = ["-reorder"]
        verbose_name = "新闻及通知"
        verbose_name_plural = "新闻及通知"


class ImageFile(models.Model):
    """ 图片表 """
    img = models.ImageField("图片", upload_to="%Y%m/images/")
    summary = models.CharField("图片名称", max_length=200)

    # 复合关联
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = "system_images"
        verbose_name = "图片表"
        verbose_name_plural = "图片表"
