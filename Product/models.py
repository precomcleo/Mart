from django.db import models
from django.contrib import admin


# Create your models here.
class Product(models.Model):  
    product_id = models.IntegerField(primary_key=True, verbose_name='商品id')
    stock_pcs = models.IntegerField(null=False, verbose_name='商品庫存數量')
    price = models.IntegerField(null=False, verbose_name='商品單價')
    shop_id = models.CharField(max_length=5, null=False, verbose_name='商品所屬館別')
    vip = models.BooleanField(default=False, verbose_name='True => VIP限定/ False =>無限制購買對象')

class Order(models.Model):  
    id = models.AutoField(primary_key=True, verbose_name='訂單id')
    product_id = models.IntegerField(null=False, verbose_name='商品id')
    qty = models.IntegerField(null=False, verbose_name='購買數量')
    price = models.IntegerField(null=False, verbose_name='商品單價')
    shop_id = models.CharField(max_length=5, null=False, verbose_name='商品所屬館別')