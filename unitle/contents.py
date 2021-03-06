# 系统模块-轮播图
SLIDER_TYPES_INDEX = 11
SLIDER_TYPES_CHOICES = (
    (SLIDER_TYPES_INDEX, "首页"),
)
# 系统模块-新闻，通知
NEWS_TYPES_NEW = 11
NEWS_TYPES_NOTICE = 12
NEWS_TYPES_CHOICES = (
    (NEWS_TYPES_NEW, "新闻"),
    (NEWS_TYPES_NOTICE, "通知"),
)

# 用户模块-性别
SEX_CHOICES = (
    ("1", "男"),
    ("0", "女"),
)

# 商品的类型
PRODUCT_TYPE_ACTUAL = 11
PRODUCT_TYPE_VIRTUAL = 12
PRODUCT_TYPES_CHOICES = (
    (PRODUCT_TYPE_ACTUAL, '实物商品'),
    (PRODUCT_TYPE_VIRTUAL, '虚拟商品'),
)


# 商品的状态
PRODUCT_STATUS_SELL = 11
PRODUCT_STATUS_LOST = 12
PRODUCT_STATUS_OFF = 13
PRODUCT_STATUS_CHOICES = (
    (PRODUCT_STATUS_SELL, '销售中'),
    (PRODUCT_STATUS_LOST, '已售完'),
    (PRODUCT_STATUS_OFF, '已下架'),
)


# 订单状态
ORDER_STATUS_INIT = 10
ORDER_STATUS_SUBMIT = 11
ORDER_STATUS_PAIED = 12
ORDER_STATUS_SENT = 13
ORDER_STATUS_DONE = 14
ORDER_STATUS_DELETED = 15
ORDER_STATUS_CHOICES = (
    (ORDER_STATUS_INIT, '购物车'),
    (ORDER_STATUS_SUBMIT, '已提交'),
    (ORDER_STATUS_PAIED, '已支付'),
    (ORDER_STATUS_SENT, '已发货'),
    (ORDER_STATUS_DONE, '已完成'),
    (ORDER_STATUS_DELETED, '已删除'),
)

# 用户登录保存在session的user_id
LOGIN_SESSION_ID = "user_id"
