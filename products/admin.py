from django.contrib import admin
from .models import Products,Stock,Receiving
# Register your models here.

class ReceivingInline(admin.TabularInline):
    model = Receiving
    extra =0
    max_num=3

class StockInline(admin.TabularInline):
    model =Stock
    extra =0
    max_num=3

class ProductAdmin(admin.ModelAdmin):
    
    inlines =[
        ReceivingInline,StockInline
    ]
    
class StockAdmin(admin.ModelAdmin):
    list_display =['product','inventory']
    readonly_fields = ['inventory']

admin.site.register(Products, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Receiving)