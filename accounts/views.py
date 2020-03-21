from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from accounts.forms import UserLoginForm, UserRegisterForm,  UserAddressForm
from accounts.models import User, UserAddress
from unitle import contents


def user_login(request):
    # 如果用户未登录编辑页面  先跳转到登录页面  再跳转编辑页
    next_url = request.GET.get("next", "index")
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            # 执行登录
            date = form.cleaned_data
            """ 自定义登录 """
            # # 获取到用户信息
            # user = User.objects.get(username=date["username"], password=date["password"])
            # request.session[contents.LOGIN_SESSION_ID] = user.id
            # return redirect("index")

            """ 使用django   auth模块登录 """
            user = authenticate(request, username=date["username"], password=date["password"])
            if user is not None:
                login(request, user)
                return redirect(next_url)
        else:
            print(form.errors)
    else:
        form = UserLoginForm(request=request)
    return render(request, "login.html", {
        "form": form,
        "next_url": next_url,
    })


def user_regist(request):
    if request.method == "POST":
        form = UserRegisterForm(request=request, data=request.POST)
        if form.is_valid():
            # 执行登录
            # 调用注册方法
            form.regist()
            return redirect("index")
        else:
            print(form.errors)
    else:
        form = UserRegisterForm(request=request)
    return render(request, "regist.html", {
        "form": form,
    })


def user_logout(request):
    logout(request)
    return redirect("index")


@login_required
def user_address(request):
    # 查询所有地址
    my_addr_list = UserAddress.objects.filter(is_valid=True, user=request.user)
    return render(request, "address_list.html", {
        "my_addr_list": my_addr_list,
    })


@login_required
def address_edit(request, pk):
    """ 地址新增或者是编辑 """
    user = request.user
    addr = None
    initial = {}
    if pk.isdigit():
        addr = get_object_or_404(UserAddress, pk=pk, user=user, is_valid=True)
        initial["region"] = addr.get_addr()
    if request.method == 'POST':
        form = UserAddressForm(request=request, data=request.POST, initial=initial, instance=addr)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_address')
    else:
        form = UserAddressForm(request=request, instance=addr, initial=initial)
    return render(request, 'address_edit.html', {
        'form': form
    })


def address_delete(request, pk):
    addr = get_object_or_404(UserAddress, is_valid=True, user=request.user, pk=pk)
    addr.is_valid = False
    addr.save()
    return HttpResponse("OK")
