from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404

from mall.models import Product
from unitle import contents


def pro_list(request):
    # 商品列表
    # 查询商品
    product_list = Product.objects.filter(is_valid=True, status=contents.PRODUCT_STATUS_SELL)
    name = request.GET.get("name", '')
    if name:
        product_list = product_list.filter(name__icontains=name)
    return render(request, "pro_list.html", {
        "product_list": product_list,
    })


def pro_info(request, pk):
    # 商品详情
    product_info = get_object_or_404(Product, is_valid=True, uid=pk)
    # 获取到用户
    user = request.user
    addr = None
    # 判断用户是否登录
    if user.is_authenticated:
        addr = user.default_addr
    return render(request, "pro_info.html", {
        "product_info": product_info,
        "addr": addr
    })


class ProductList(ListView):
    # 每页展示的数据
    paginate_by = 6
    # 模板的位置
    template_name = "pro_list.html"

    def get_queryset(self):
        # 查询商品信息
        query = Q(is_valid=True, status=contents.PRODUCT_STATUS_SELL)
        name = self.request.GET.get("name", '')
        if name:
            query = query & Q(name__icontains=name)
        # 按标签名查找
        tag = self.request.GET.get("tag", '')
        if tag:
            query = query & Q(tags__code=tag)
        return Product.objects.filter(query)

    def get_context_data(self, *, object_list=None, **kwargs):
        # 传其他的参数到前端
        content = super().get_context_data(**kwargs)
        content["search_data"] = self.request.GET.dict()
        return content


def pro_classify(request):
    return render(request, "classify.html", {

    })




