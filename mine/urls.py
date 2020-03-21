from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from mine import views

urlpatterns = (
    # 订单页面
    url(r'^order/info/(?P<sn>\S+)/$', login_required(views.OrderInfo.as_view()), name='order_info'),
    # 加入购物车
    url(r'^car/add/(?P<uid>\S+)/$', views.car_add, name='car_add'),
    # 购物车
    url(r'^car/$', views.car, name='car'),
    # 提交订单
    url(r'^order/pay/$', views.order_pay, name='order_pay'),
    # 个人中心
    url(r'^mine/$', views.mine, name='mine'),
    # 我的收藏
    url(r'^my/collect/$', views.my_collect, name='my_collect'),
    # 订单列表
    url(r'^order/list/$', login_required(views.OrderListView.as_view()), name='order_list'),
)