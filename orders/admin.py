from django.contrib import admin
from .models import Orders,OrderItems
# Register your models here.

class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra =0
    max_num =3


class OrdersAdmin(admin.ModelAdmin):
    list_display =['order_number','status','order_total','subtotal','tax']
    inlines =[
        OrderItemsInline
    ]



admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderItems)
