import re

from django import forms
from django.contrib.auth import authenticate, login

from accounts.models import User, UserAddress
from unitle.verify import VerifyCode


class LoginForm(forms.Form):
    username = forms.CharField(label="姓名", max_length=32)


class UserLoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=64, error_messages={
        "required": "用户名不能为空",
    })
    password = forms.CharField(label="密码", max_length=255, widget=forms.PasswordInput, error_messages={
        "required": "密码不能为空",
    })
    verify_code = forms.CharField(label="验证码", max_length=4, error_messages={
        "required": "验证码不能为空",
    })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # def clean_username(self):
    #     # 钩子函数获取用户名
    #     username = self.cleaned_data["username"]
    #     # 正则匹配用户名
    #     re_username = r"^1[34578]\d{9}$"
    #     if not username:
    #         raise forms.ValidationError("用户名不能为空")
    #     if not re.search(re_username, username):
    #         raise forms.ValidationError("请输入正确的手机号码")
    #     return username

    def clean(self):
        # 重写父类的方法
        clean_date = super().clean()
        # 获取用户名和密码
        username = clean_date.get("username", None)
        password = clean_date.get("password", None)
        # 判断用户名和密码是否存在
        if username and password:
            user_list = User.objects.filter(username=username)
            if user_list.count() == 0:
                raise forms.ValidationError("用户名不存在")
            # if not user_list.filter(password=password).exists():
            #     raise forms.ValidationError("密码错误")
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("密码错误")
        return clean_date

    def clean_verify_code(self):
        code = self.cleaned_data["verify_code"]
        if not code:
            raise forms.ValidationError("验证码不能为空")
        client = VerifyCode(self.request)
        if not client.valid_code(code):
            raise forms.ValidationError("您输入的验证码不正确")
        return code


class UserRegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=64)
    password = forms.CharField(label="密码", max_length=255, widget=forms.PasswordInput)
    password_valid = forms.CharField(label="确认密码", max_length=255, widget=forms.PasswordInput)
    verify_code = forms.CharField(label="验证码", max_length=4)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_verify_code(self):
        code = self.cleaned_data["verify_code"]
        if not code:
            raise forms.ValidationError("验证码不能为空")
        client = VerifyCode(self.request)
        if not client.valid_code(code):
            raise forms.ValidationError("您输入的验证码不正确")
        return code

    def clean(self):
        clean_date = super().clean()
        password = clean_date.get("password", None)
        password_valid = clean_date.get("password_valid", None)
        if password and password_valid:
            if password != password_valid:
                raise forms.ValidationError("两次密码输入不一致")
        return clean_date

    def regist(self):
        date = self.cleaned_data
        User.objects.create_user(username=date["username"], password=date["password"])
        # 自动登录
        user = authenticate(username=date["username"], password=date["password"])
        login(self.request, user)
        return user


class UserAddressForm(forms.ModelForm):
    """" 地址新增|修改 """

    region = forms.CharField(label='大区域选项', max_length=64, required=True,
                             error_messages={
                                 'required': '请选择地址'
                             })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = UserAddress
        fields = ['address', 'username', 'phone', 'is_default']
        widgets = {
            'is_default': forms.CheckboxInput(attrs={
                'class': 'weui-switch'
            })
        }

    def clean_phone(self):
        """ 验证用户输入的手机号码 """
        phone = self.cleaned_data['phone']
        # 判断用户名是否为手机号码
        pattern = r'^0{0,1}1[0-9]{10}$'
        if not re.search(pattern, phone):
            raise forms.ValidationError('请输入正确的手机号码')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        # 查询当前登录用户的地址数据
        addr_list = UserAddress.objects.filter(is_valid=True, user=self.request.user)
        if addr_list.count() >= 20:
            raise forms.ValidationError('最多只能添加20个地址')
        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        region = self.cleaned_data['region']
        # 省市区的数据
        (province, city, area) = region.split(' ')
        obj.province = province
        obj.city = city
        obj.area = area
        obj.user = self.request.user

        # 修改的时候，如果已经有了默认地址，当前也勾选了默认地址选项
        # 需要把之前的地址都改为非默认的地址
        if self.cleaned_data['is_default']:
            UserAddress.objects.filter(is_valid=True, user=self.request.user, is_default=True).update(is_default=False)
        obj.save()






