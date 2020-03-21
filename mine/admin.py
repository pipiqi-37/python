from django.contrib import admin

# Register your models here.
from mine.models import Order, Cart, Comments


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["sn", "user", "buy_count", "buy_amount", "express_type", "express_no", "status"]
    search_fields = ["user__username"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ["user", "product", "name", "count", "amount"]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["product", "desc"]
