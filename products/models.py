import uuid
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save,pre_save
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default =uuid.uuid4, editable =False)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='products',null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug =slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("products:products_detail", kwargs={"slug": self.slug})
    
        




class Stock(models.Model):
    product = models.ForeignKey(Products, on_delete=models.RESTRICT)
    inventory = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product)

    

class Receiving(models.Model):
    product =models.ForeignKey(Products, on_delete =models.DO_NOTHING)
    quantity =models.IntegerField(default =0)
    

def post_save_Receiving(sender, instance, *args, **kwargs):
    receiving =instance
    product = instance.product 
    stock =Stock.objects.filter(product= product)
    if stock.exists():
        stock = stock.first()
        stock.inventory += instance.quantity
        stock.save()
    else:
        Stock.objects.create(product=product, inventory=instance.quantity)
        


post_save.connect(post_save_Receiving, sender=Receiving)


def pre_save_Receiving(sender ,instance, *args, **kwargs):
    receiving =instance
    product = instance.product
    
    if instance.id is not None:
        stock =Stock.objects.filter(product=product)
        stock =stock.first()
        pre_receiving =Receiving.objects.get(id=instance.id)
        stock.inventory -= pre_receiving.quantity
        stock.save()

pre_save.connect(pre_save_Receiving, sender=Receiving)








