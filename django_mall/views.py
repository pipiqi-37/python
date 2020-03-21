from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import User
from mall.models import Product
from system.models import Slider, News
from unitle import contents


def index(request):
    # 轮播图
    slider_img = Slider.objects.filter(types=contents.SLIDER_TYPES_INDEX,
                                       is_valid=True)
    # 新闻-通知
    now_time = datetime.now()
    news_list = News.objects.filter(types=contents.NEWS_TYPES_NEW,
                                    is_valid=True,
                                    is_top=True,
                                    start_time__lte=now_time,
                                    end_time__gte=now_time)

    # 将分类的信息渲染到首页分类
    jstj_list = Product.objects.filter(is_valid=True, status=contents.PRODUCT_STATUS_SELL, tags__code="jstj")
    jxtj_list = Product.objects.filter(is_valid=True, status=contents.PRODUCT_STATUS_SELL, tags__code="jxtj")
    cnxh_list = Product.objects.filter(is_valid=True, status=contents.PRODUCT_STATUS_SELL, tags__code="cnxh")
    # # 从session里获取到用户ID
    # user_id = request.session[contents.LOGIN_SESSION_ID]
    # # 通过用户ID找到登录的用户
    # user = User.objects.get(pk=user_id)
    # if not user:
    #     print(403)
    return render(request, 'index.html', {
        "slider_img": slider_img,
        "news_list": news_list,
        "jstj_list": jstj_list,
        "jxtj_list": jxtj_list,
        "cnxh_list": cnxh_list,
        # "user": user,
    })

