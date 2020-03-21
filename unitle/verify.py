import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

from django_mall import settings


class VerifyCode(object):
    """ 验证码 """
    def __init__(self, dj_request):
        # 请求
        self.dj_request = dj_request
        # 验证码的长度
        self.code_len = 4
        # 验证码图片的长，高
        self.img_with = 100
        self.img_height = 40

        self.session_name = "verify_code"

    def gen_code(self):
        """ 生成验证码 """
        # 获取生成的验证码
        code = self.get_code()
        # 将获取的到的验证码保存到session中
        self.dj_request.session[self.session_name] = code
        # 生成字体随机色
        fonts_color = ["blue", "red", "orange", "green", "purple", "grey", "pink", "yellow", "Cyan"]
        # 生成背景随机色
        bg_color = (random.randint(230, 255), random.randint(230, 255), random.randint(230, 255))
        # 加载字体路径
        fonts_path = os.path.join(settings.BASE_DIR, "static", "fonts", "timesbi.ttf")

        # 创建图片
        img = Image.new("RGB", (self.img_with, self.img_height), bg_color)
        draw = ImageDraw.Draw(img)

        # 画干扰线
        line_color = random.choice(fonts_color)
        for i in range(random.randrange(1, int(self.code_len / 2) + 1)):
            line_color = random.choice(fonts_color)
            # 线条的位置
            point = (random.randrange(0, self.img_with * 0.2),
                     random.randrange(0, self.img_height * 0.2),
                     random.randrange(self.img_with - self.img_with * 0.2, self.img_with),
                     random.randrange(self.img_height - self.img_height * 0.2, self.img_height))
            # 线条的宽度
            line_width = random.randrange(1, 5)
            # 渲染线条
            draw.line(point, fill=line_color, width=line_width)

        # 画验证码
        for index, char in enumerate(code):
            code_color = random.choice(fonts_color)
            font_size = random.randrange(15, 20)
            font = ImageFont.truetype(fonts_path, font_size)
            local_code = (index * self.img_with / self.code_len,
                          random.randrange(0, self.img_height / 2))
            draw.text(local_code, char, fill=code_color, font=font)

        # 将图片加载到IO流
        buf = BytesIO()
        img.save(buf, "gif")
        return HttpResponse(buf.getvalue(), "image/gif")

    def get_code(self):
        code_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        code_list = random.sample(list(code_str), self.code_len)
        # 拼接列表,生成四位数的验证码
        code = "".join(code_list)
        return code

    def valid_code(self, code):
        """ 验证验证码 """
        # 转换小写
        code = str(code).lower()
        # 从session里取验证码
        vcode = self.dj_request.session.get(self.session_name, "")
        if vcode.lower() == code:
            return True
        return False


if __name__ == '__main__':
    a = VerifyCode(None)
    a.gen_code()