from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, UserAddress, UserProfile
from unitle.admin_active import disable_user, enable_user


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["format_username", "integral", "is_active"]
    search_fields = ["username"]

    # 将自定义方法渲染到页面
    actions = ["disable_user", "enable_user"]
    # 后台添加属性
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name',
                                        'email', 'integral')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def format_username(self, user):
        return user.username[:3] + "***"
    # 修改列明 显示
    format_username.short_description = "用户名"

    def disable_user(self, request, queryset):
        # 批量禁用用户
        queryset.update(is_active=False)
    disable_user.short_description = "批量禁用用户"

    def enable_user(self, request, queryset):
        queryset.update(is_active=True)
    enable_user.short_description = "批量启用用户"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "email", "phone_num", "sex", "age"]
    search_fields = ["user"]


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ["province", "city", "area", "town", "address", "username", "phone"]
    actions = [disable_user, enable_user]

