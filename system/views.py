from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404

# Create your views here.
from system.models import News
from unitle import contents
from unitle.verify import VerifyCode


def news_list(request):
    """ 新闻列表 """
    # 获取当前页码
    page = request.GET.get("page", 1)
    # 每一页放多少数据
    page_size = 10
    news = News.objects.filter(types=contents.NEWS_TYPES_NEW,
                               is_valid=True)
    # 创建一个分页器
    paginator = Paginator(news, page_size)
    # 对页面进行分页
    page_date = paginator.page(page)
    return render(request, "news_list.html", {
        "page_date": page_date,
    })


def news_detail(request, pk):
    # 新闻详情
    news_info = get_object_or_404(News, pk=pk, is_valid=True)
    # 浏览一次加一次
    news_info.view_count = F("view_count") + 1
    # 保存至数据库
    news_info.save()
    # 刷新数据库
    news_info.refresh_from_db()
    return render(request, "news_info.html", {
        "news_info": news_info,
    })


def verify_code(request):
    code = VerifyCode(request)
    return code.gen_code()