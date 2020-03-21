from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.db.models import Sum, Q
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.db import transaction
# Create your views here.
from django.views.generic import DetailView, ListView

from mall.models import Product
from mine.models import Order, Cart
from unitle import contents, order_sn


class OrderInfo(DetailView):
    model = Order
    slug_field = 'sn'
    slug_url_kwarg = 'sn'
    template_name = "order_info.html"


@login_required
@transaction.atomic()
def car_add(request, uid):
    pro_list = get_object_or_404(Product, uid=uid,
                                 is_valid=True,
                                 status=contents.PRODUCT_STATUS_SELL)
    # 获取购买数量
    count = int(request.POST.get("count", 1))
    # 校验库存  不能小于购买数量
    if pro_list.ramain_count < count:
        return HttpResponse("库存不足")
    # 调整库存数量  减库存
    pro_list.update_store_count(count)
    # 生成购物车信息
    try:
        # 如果购物车有该商品信息  则数量增加  总价增加
        cart = Cart.objects.get(product=pro_list, user=request.user, status=contents.ORDER_STATUS_INIT)
        cart.count = cart.count + count
        cart.amount = cart.price * cart.count
        cart.save()
        cart.refresh_from_db()
    except Cart.DoesNotExist:
        # 没有商品信息则创建
        Cart.objects.create(user=request.user,
                            product=pro_list,
                            name=pro_list.name,
                            price=pro_list.price,
                            count=count,
                            img=pro_list.img,
                            origin_price=pro_list.origin_price,
                            amount=count * pro_list.price)

    return HttpResponse("OK")


@login_required
def car(request):
    user = request.user
    pro_list = user.carts.filter(status=contents.ORDER_STATUS_INIT)
    if request.method == "POST":
        default_addr = user.default_addr
        if not default_addr:
            # 没有地址消息提示
            messages.warning(request, "请选择地址信息")
            return redirect("accounts:address_edit")
        # 计算商品的总额和数量
        cart_total = pro_list.aggregate(sum_amount=Sum('amount'), sum_count=Sum('count'))
        # 生成随机的订单号
        sn = order_sn.order_sn()
        order = Order.objects.create(
                                    sn=sn,
                                    user=user,
                                    buy_count=cart_total["sum_count"],
                                    buy_amount=cart_total["sum_amount"],
                                    to_user=default_addr.username,
                                    to_area=default_addr.get_addr(),
                                    to_address=default_addr.address,
                                    to_phone=default_addr.phone
        )
        messages.success(request, "下单成功，请及时支付")
        pro_list.update(status=contents.ORDER_STATUS_SUBMIT, order=order)

        return redirect("mine:order_info", order.sn)
    return render(request, 'shopcart.html', {
        "pro_list": pro_list,
    })


@login_required
def order_pay(request):
    # 提交订单
    user = request.user
    if request.method == "POST":
        sn = request.POST.get("sn", '')
        # 1 查询订单信息
        order = get_object_or_404(Order, user=user, sn=sn)
        # 2 判断用户积分
        if order.buy_amount > user.integral:
            messages.error(request, "账户积分不足")
            return redirect('mine:order_info', sn=sn)
        # 扣除积分
        user.integral_account(0, order.buy_amount)
        # 变更订单状态
        order.status = contents.ORDER_STATUS_PAIED
        # 修改购物车中商品的状态
        order.carts.all().update(status=contents.ORDER_STATUS_PAIED)
        order.save()
        messages.success(request, "支付成功")
    return redirect('mine:order_list')


@login_required
def mine(request):
    # 获取用户的订单
    user = request.user
    return render(request, "mine.html", {
        "contents": contents,
        "user" : user
    })


@login_required
def my_collect(request):
    return render(request, "shoucang.html", {

    })


# @login_required
# def order_list(request):
#     # user = request.user
#     # order_status = Order.objects.filter().exclude(status=contents.ORDER_STATUS_INIT)
#     # # 1 查询订单数据
#     # all_order_list = Order.objects.filter(user=user, status=order_status)
#     # # 2 分页
#     # page = request.GET.get("page", 1)
#     # page_size = 5
#     # # 创建分页器
#     # paginator = Paginator(all_order_list, page_size)
#     # page_data = paginator.page(page)
#     status = request.GET.get("status", '')
#     try:
#         status = int(status)
#     except ValueError:
#         status = ""
#     return render(request, "order_list.html", {
#         "contents": contents,
#         "status": status
#
#     })


class OrderListView(ListView):
    model = Order
    template_name = "order_list.html"

    def get_queryset(self):
        status = self.request.GET.get("status", '')
        user = self.request.user
        query = Q(user=user)
        if status:
            query = query & Q(status=status)
        return Order.objects.filter(query).exclude(status=contents.ORDER_STATUS_DELETED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get("status", '')
        try:
            status = int(status)
        except ValueError:
            status = ""
        context["status"] = status
        context["contents"] = contents
        return context


