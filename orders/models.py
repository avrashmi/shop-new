import uuid
from django.db import models
from products.models import Products,Stock
from django.db.models.signals import post_save,pre_save,pre_delete
from django.db.models import Sum
import decimal 
from django.core.exceptions import ValidationError

# Create your models here.
ORDER_STATUS=[
    (0,'cart'),
    (1,'pending'),
    (2,'paid'),
    (3,'shipped'),
    (4,'delivered'),
    (5,'canceled'),
    (6,'refunded'),
]

class Orders(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(default=0, choices=ORDER_STATUS)
    order_total = models.DecimalField(max_digits=5, decimal_places=2, default =0.00)
    subtotal = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)

    def __str__(self):
        return str(self.product)
   
    def save(self, *args, **kwargs):
        self.line_total = self.product.price * self.quantity
        super().save(*args , **kwargs)
    
    def clean(self):
        stock = Stock.objects.filter(product =self.product)
        if stock.exists():
            stock =stock.first()
            if stock.inventory < self.quantity:
                raise ValidationError({'quantity':f'max available:{stock.inventory}'})
        else:
            raise ValidationError({'quantity':'Sufficient quantity not available'})



        

'''def post_save_OrderItems(sender, instance, *args, **kwargs):
    orderItem = instance  #the object which is saved-the current object
    order = instance.order
    orderedItems = OrderItems.objects.filter(order=order)
    total =decimal.Decimal(0.00)
    for item in orderedItems:
        total += item.line_total
    order.subtotal =total
    order.save()'''

def post_save_OrderItems(sender, instance, *args, **kwargs):
    order = instance.order
    # ordered_items =order.orderitems_set.aggregate(order_total=Sum('line_total'))
    ordered_items =order.items.aggregate(order_total=Sum('line_total'))
    order.subtotal =ordered_items['order_total']
    order.save()
    
    
    stock =Stock.objects.filter(product =instance.product)
    if stock.exists():
        stock = stock.first()
        stock.inventory -= instance.quantity
        stock.save()

    


post_save.connect(post_save_OrderItems,sender=OrderItems)


def pre_save_OrderItems(sender, instance, *args, **kwargs):
    order = instance.order

    if instance.id is not None:
        stock = Stock.objects.filter(product = instance.product)
        if stock.exists():
            stock = stock.first()
            pre_orderItems =OrderItems.objects.get(id= instance.id)
            stock.inventory += pre_orderItems.quantity
            stock.save()

pre_save.connect(pre_save_OrderItems, sender=OrderItems)
pre_delete.connect(pre_save_OrderItems, sender=OrderItems)












