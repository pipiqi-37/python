from django.conf.urls import url

from mall import views

urlpatterns = (

    # 商品列表
    # url(r'^pro/list/$', views.pro_list, name='pro_list'),

    # 商品列表 用class来实现
    url(r'^pro/list/$', views.ProductList.as_view(), name='pro_list'),
    # 分页-商品列表的片段
    url(r'^pro/load/list/$', views.ProductList.as_view(
        template_name="pro_load_list.html"
    ), name='pro_load_list'),

    # 商品详情
    url(r'^pro/info/(?P<pk>\S+)/$', views.pro_info, name="pro_info"),
    # 商品分类
    url(r'^pro/classify/$', views.pro_classify, name='pro_classify'),

)