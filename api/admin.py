from django.contrib import admin
from api.models import Product,User,Orders,Cart,UserProduct#,Purchasing
# from django.contrib.auth.admin import UserAdmin
# from .models import User
#
# admin.site.register(User, UserAdmin)

# Register your models here.
#
# admin.site.register(Product)# class ProductAdmin(admin.ModelAdmin):
admin.site.register(Cart)# class ProductAdmin(admin.ModelAdmin):
admin.site.register(Orders)# class ProductAdmin(admin.ModelAdmin):
# admin.site.register(User)# class ProductAdmin(admin.ModelAdmin):
# class ProductAdmin(admin.ModelAdmin):
#     # list_display = ('name',)

@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_filter = ['product',]
    list_display = ['product','buy_quantity','rating']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'category_name', 'quantity')
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name',)
#     pass
