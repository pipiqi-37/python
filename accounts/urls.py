from django.conf.urls import url

from accounts import views

urlpatterns = [
    # 用户登录
    url(r"^user/login/$", views.user_login, name="user_login"),
    # 用户退出
    url(r"^user/logout/$", views.user_logout, name="user_logout"),
    # 用户注册
    url(r"^user/regist/$", views.user_regist, name="user_regist"),
    # 地址列表
    url(r"^user/address/$", views.user_address, name="user_address"),
    # 新增收获地址
    url(r"^user/address/edit/(?P<pk>\S+)/$", views.address_edit, name="address_edit"),
    # 删除地址
    url(r"^user/address/delete/(?P<pk>\S+)/$", views.address_delete, name="address_delete"),
]