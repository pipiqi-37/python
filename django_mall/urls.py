"""django_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin




# import xadmin

from django_mall import views

# xadmin.autodiscover()

# # version模块自动注册需要版本控制的 Model
# from xadmin.plugins import xversion
# xversion.register_models()


urlpatterns = [
    url('admin/', admin.site.urls),
    # xadmin配置
    # url('xadmin/', xadmin.site.urls),

    url(r'^$', views.index, name='index'),

    # 商品部分
    url(r'^mall/', include(('mall.urls', 'mall'), namespace='mall')),

    # 系统部分
    url(r'^system/', include(('system.urls', "system"), namespace='system')),

    # 用户中心
    url(r'^accounts/', include(('accounts.urls', "accounts"), namespace='accounts')),

    # 个人中心
    url(r'^mine/', include(('mine.urls', "mine"), namespace='mine')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
