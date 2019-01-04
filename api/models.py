from django.db import models
import math
from datetime import datetime,timedelta
import time
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.validators import validate_neg_quantity,validate_quantity,validate_max_quantity,validate_phoneno

# from django.contrib.auth.models import AbstractUser

class Product(models.Model):

    CATEGORY = (
    ('Fashion','Fashion'),
    ('Sports','Sports'),
    ('Books','Books'),
    ('Home & Kitchen','Home & Kitchen'),
    ('Computers, Laptops, Mobiles & Accessories','Computers, Laptops, Mobiles & Accessories'),
    ('Beauty','Beauty'),
    ('Automobile','Automobile'),
    ('Toys & Kids Stuff','Toys & Kids Stuff'),
    ('Grocery & Pantry','Grocery & Pantry'),
    )

    added = models.DateTimeField(auto_now_add=True)
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50,blank=False)#,unique=True)
    category_name = models.CharField(choices = CATEGORY,max_length = 50,blank=False,default = None)
    description = models.TextField(blank=False)
    buy_price = models.DecimalField(blank=False,max_digits=7,decimal_places=2)
    sell_price = models.DecimalField(blank=False,max_digits=7,decimal_places=2)
    quantity = models.IntegerField(blank=False,validators=[validate_quantity,validate_neg_quantity])
    rating = models.DecimalField(max_digits=2,decimal_places=1,default=-1)
    buy_quantity = models.IntegerField(default=0,blank=False,validators=[validate_neg_quantity,validate_max_quantity])

    def __str__(self):
        return (self.name)

    def id(self):
        return self.product_id
#
class UserProduct(models.Model):
    STAR_CHOICES = [(-1,-1),(1,1),(2,2),(3,3),(4,4),(5,5)]
    rating = models.IntegerField(choices = STAR_CHOICES,default=-1)
    # review = models.CharField(max_length = 100,blank = True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    buy_quantity = models.IntegerField(default=0,blank=False)

    def __str__(self):
        return self.product.name

class User(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # count = models.IntegerField()
    def name(self):
        return self.user.username

class Cart(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,blank=True)
    address = models.CharField(max_length=100,blank=True,null=True,default = None)
    phone_no = models.BigIntegerField(validators=[validate_phoneno],blank=True,null=True,default=None)
    def __str__(self):
        return str(self.id)

    # print(Cart.products.count())

    def product_list(self):
        # return (self.products.count())
        total_products = self.products.all().count()
        # return total_products
        l = []
        for i in range(total_products):
            dic = {}
            if self.products.all()[i].buy_quantity != 0:
                dic['product_name'] = (self.products.all())[i].name
                dic['price'] = (self.products.all())[i].sell_price
                l.append(dic)
        return l

class Orders(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,blank=True)
