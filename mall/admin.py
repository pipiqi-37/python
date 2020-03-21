from django.contrib import admin

# Register your models here.
from mall.forms import ProAdmin
from mall.models import Product, Tag, Classify
from unitle.admin_active import disable_user, enable_user


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "desc", "types", "price", "status", "is_valid"]
    list_per_page = 5
    # 按照商品的状态搜索
    list_filter = ("status", )
    # 字段信息只读， 不可编辑
    readonly_fields = ["ramain_count", "uid"]

    actions = [disable_user, enable_user]
    # 自定义表单
    form = ProAdmin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "uid", "code", "is_valid"]
    actions = [disable_user, enable_user]


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    list_display = ["name", "desc"]
    actions = [disable_user, enable_user]