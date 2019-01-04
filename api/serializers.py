from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator
from api.validators import validate_add_quantity
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from api.validators import validate_neg_quantity,validate_quantity,validate_max_quantity,validate_phoneno,validate_address
from api.models import Product,Cart,Orders,UserProduct
from django.contrib.auth import get_user_model
from rest_framework import serializers
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id','name','category_name','description','buy_price','sell_price','quantity','rating')


class ProductCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=Product.objects.all())])
    class Meta:
        model = Product
        fields = ('product_id','name','category_name','description','buy_price','sell_price','quantity')

class ProductUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=Product.objects.all())])
    class Meta:
        model = Product
        fields = ('product_id','name','category_name','description','buy_price','sell_price','quantity')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.description = validated_data.get('description', instance.description)
        instance.buy_price = validated_data.get('buy_price', instance.buy_price)
        instance.sell_price = validated_data.get('sell_price', instance.sell_price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class ProductCartSerializer(serializers.ModelSerializer):
    # quantity = serializers.IntegerField(validators = [validate_neg_quantity])
    class Meta:
        model = Product
        fields = ('product_id','id','name','sell_price','buy_quantity')#,'quantity')
        extra_kwargs = {"sell_price":
                            {"read_only":"True"},
                            }

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=20,required=True)
    last_name = serializers.CharField(max_length=20,required=True)

    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password']#,'is_superuser','is_staff']
        extra_kwargs = {"password":
                          {"write_only":True},
                          }
    def create(self,validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        # is_staff = validated_data['is_staff']
        # is_admin = validated_data['is_admin']
        user_obj = User(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            # is_superuser = True,
            # is_staff = True,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

User = get_user_model()
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class CartSerializer(serializers.ModelSerializer):
    # products = ProductSerializer
    class Meta:
        model = Cart
        fields = ('id','products','product_list')#,'subtotal_amount','total_amount')

class CartProductSerializer(serializers.HyperlinkedModelSerializer):
    products = ProductCartSerializer(required=False,many=True)
    id = serializers.ReadOnlyField()
    class Meta:
        model = Cart
        fields = ('id','products')#,'subtotal_amount','total_amount')#,'product_list','subtotal_amount','total_amount')
        # extra_kwargs = {"products":
        #                     {"write_only":True}
        #                     }
    def update(self, instance, validated_data):
        cart = Cart.objects.get(id=instance.id)
        # products = cart.products.all()
        # for i in range(products.count()):
        products = validated_data.pop(('products'))
        # print(products)
        for i in range(len(products)):
            # print(products[i])
            product = Product.objects.get(name=products[i]['name'])
            # print(product)
            user_products = UserProduct.objects.all()
            all_product_objects = UserProduct.objects.filter(product = product.product_id)
            # print(all_product_objects)
            user_product_id = all_product_objects[(instance.id)-1].id
            user_product = UserProduct.objects.get(id = user_product_id)
            earlier_quantity = user_product.buy_quantity
            user_product.buy_quantity = products[i]['buy_quantity']
            product.quantity -= (user_product.buy_quantity-earlier_quantity)
            user_product.save()
            product.save()
        return instance

# class CartCheckoutSerializer(serializers.HyperlinkedModelSerializer):
#     products = ProductCartSerializer(required=False,many=True)
#     # address = serializers.CharField(required=True)
#     # phone_no = serializers.CharField(validators=[validate_phoneno],required=True)
#     id = serializers.ReadOnlyField()
#     class Meta:
#         model = Cart
#         fields = ('id','products')
#         # fields = ('id','address','phone_no')
#     def update(self, instance, validated_data):
#         all_user_products = UserProduct.objects.all()
#         for all_user_products in UserProduct.objects.all():
#             last_added_id = all_user_products.id
#         for i in range(last_added_id):
#             user_product_exists = UserProduct.objects.filter(id = i+1).exists()
#             if user_product_exists:
#                 user_product = UserProduct.objects.get(id=i+1)
#                 user_product.buy_quantity = 0
#                 user_product.save()
#         # address.instance = validated_data.get('address',instance.address)
#         # phone_no.instance = validated_data.get('phone_no',instance.phone_no)
#         # instance.save()
#         return instance
class CartCheckoutSerializer(serializers.HyperlinkedModelSerializer):
    products = ProductCartSerializer(required=False,many=True)
    id = serializers.ReadOnlyField()
    address = serializers.CharField(validators = [validate_address])
    phone_no = serializers.CharField(required = True)
    class Meta:
        model = Cart
        fields = ('id','products','address','phone_no')#,'subtotal_amount','total_amount')#,'product_list','subtotal_amount','total_amount')
        # extra_kwargs = {"products":
        #                     {"write_only":True}
        #                     }
    def update(self, instance, validated_data):
        all_user_products = UserProduct.objects.all()
        for all_user_products in UserProduct.objects.all():
            last_added_id = all_user_products.id


        for i in range(last_added_id):
            user_product_exists = UserProduct.objects.filter(id = i+1).exists()
            if user_product_exists:
                user_product = UserProduct.objects.get(id=i+1)
                user_product.buy_quantity = 0
                user_product.save()
        instance.address = validated_data.get('address',instance.address)
        instance.phone_no = validated_data.get('phone_no',instance.phone_no)
        instance.save()
        return instance
User = get_user_model()
# class UserLoginSerializer(serializers.HyperlinkedModelSerializer):
#     id = serializers.ReadOnlyField()
#     class Meta:
#         model = User
#         fields = ['username','password']
#
#     def post(self,validated_data):
#         username = validated_data.pop(('username'))
#         username = validated_data.pop(('username'))


class RateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProduct
        fields = ('rating',)
