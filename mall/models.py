from django.db import models


import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField
# from accounts.models import User
from django.db.models import F

from system.models import ImageFile
from unitle import contents


class Classify(models.Model):
    """ 商品的分类 """
    uid = models.UUIDField('分类ID', default=uuid.uuid4)
    parent = models.ForeignKey('self', related_name='children')
    img = models.ImageField('分类主图', upload_to='classify')
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    desc = models.CharField('描述', max_length=64, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mall_classify'
        verbose_name = "商品的分类"
        verbose_name_plural = "商品的分类"


class Tag(models.Model):
    """ 商品的标签 """

    uid = models.UUIDField('标签ID', default=uuid.uuid4)
    img = models.ImageField('主图', upload_to='tags', null=True, blank=True)
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mall_tag'
        verbose_name = "商品标签"
        verbose_name_plural = "商品标签"

    def __str__(self):
        return '{}: {}'.format(self.code, self.name)


class Product(models.Model):
    """ 商品 """
    uid = models.UUIDField('商品ID', default=uuid.uuid4)
    name = models.CharField('商品名称', max_length=128)
    desc = models.CharField('简单描述', max_length=256, null=True, blank=True)

    # content = models.TextField('商品描述')
    # 商品富文本展示
    content = RichTextField('商品描述')

    types = models.SmallIntegerField('商品类型',
                                     choices=contents.PRODUCT_TYPES_CHOICES,
                                     default=contents.PRODUCT_TYPE_ACTUAL)
    price = models.IntegerField('兑换价格（积分兑换）')
    origin_price = models.FloatField('原价')
    img = models.ImageField('主图', upload_to='%Y%m/product')
    buy_link = models.CharField('购买链接', max_length=256, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    status = models.SmallIntegerField('商品状态', default=contents.PRODUCT_STATUS_LOST,
                                      choices=contents.PRODUCT_STATUS_CHOICES)

    sku_count = models.IntegerField('库存', default=0)
    ramain_count = models.IntegerField('剩余库存', default=0)
    view_count = models.IntegerField('浏览次数', default=0)
    score = models.FloatField('商品的评分', default=10.0)

    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    tags = models.ManyToManyField(Tag, verbose_name='标签',
                                  related_name='tags'
                                  )
    classes = models.ManyToManyField(Classify, verbose_name='分类',
                                     related_name='classes')
    # 反向关联
    banners = GenericRelation(ImageFile, verbose_name='banner图',
                              related_query_name='banners')

    class Meta:
        db_table = 'mall_product'
        ordering = ['-reorder']
        verbose_name = "商品信息"
        verbose_name_plural = "商品信息"

    def update_store_count(self, count):
        """ 更改商品的库存 """
        # 减库存
        self.ramain_count = F("ramain_count") - abs(count)
        self.save()
        self.refresh_from_db()

    def __str__(self):
        return self.name


