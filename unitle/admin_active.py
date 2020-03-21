from django.contrib import messages


def disable_user(self, request, queryset):
    # 批量禁用用户
    queryset.update(is_valid=False)
    messages.success(request, "操作成功")


disable_user.short_description = "批量禁用所选对象"


def enable_user(self, request, queryset):
    queryset.update(is_valid=True)
    messages.success(request, "操作成功")


enable_user.short_description = "批量启用所选对象"
