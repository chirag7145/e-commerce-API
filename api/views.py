from api.permissions import IsOwnerOrReadOnly
from api.models import Product,User,Cart,Orders,UserProduct
from rest_framework import mixins
from api.serializers import ProductDetailSerializer,ProductCreateSerializer,ProductUpdateSerializer,UserSerializer,UserDetailSerializer,CartSerializer,CartProductSerializer,CartCheckoutSerializer,RateProductSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model,login,authenticate
from django.http import Http404
from rest_framework.permissions import (AllowAny,IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly)
import math

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product)
        product = Product.objects.get(product_id = pk)
        all_user_products = UserProduct.objects.filter(product = product)
        rating_list = []
        for i in range(len(all_user_products)):
            if all_user_products[i].rating != -1:
                rating_list.append(all_user_products[i].rating)
        if len(rating_list) > 0:
            rating = sum(rating_list)/len(rating_list)
            product.rating = rating
            product.save()
            return Response(serializer.data)
            # return Response({"id":serializer.data['product_id'],"name":serializer.data['name'],"category_name":serializer.data['category_name'],"description":serializer.data['description'],"buy_price":serializer.data['buy_price'],"sell_price":serializer.data['sell_price'],"quantity":serializer.data['quantity'],"rating":rating})
        return Response({"id":serializer.data['product_id'],"name":serializer.data['name'],"category_name":serializer.data['category_name'],"description":serializer.data['description'],"buy_price":serializer.data['buy_price'],"sell_price":serializer.data['sell_price'],"quantity":serializer.data['quantity']})

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    def post(self, request, format=None):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            last_added_id = 0
            all_products = Product.objects.all()
            all_carts = Cart.objects.all()
            for all_carts in Cart.objects.all():
                last_added_id = all_carts.id
            for i in range(last_added_id):
                cart_exists = Cart.objects.filter(id = i+1).exists()
                if cart_exists :
                    cart = Cart.objects.get(id = i+1)
                    cart.products.set(all_products)
            all_carts = Cart.objects.all()
            for all_products in Product.objects.all():
                last_added_id = all_products.product_id
            latest_product = Product.objects.get(product_id = last_added_id)
            for i in range((all_carts.count())):
                UserProduct.objects.create(product = latest_product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_messages = serializer.errors
            error_list = list(serializer.errors)
            error_message = list(serializer.errors[error_list[0]])[0]
            error = {"status": "failure", "reason": error_message }
            return Response((error), status=status.HTTP_400_BAD_REQUEST)

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductUpdate(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product)
        if serializer.data['rating'] == -1:
            return Response({"id":serializer.data['id'],"name":serializer.data['name'],"category_name":serializer.data['category_name'],"description":serializer.data['description'],"buy_price":serializer.data['buy_price'],"sell_price":serializer.data['sell_price'],"quantity":serializer.data['quantity']})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            value = {"status":"updated"}
            return Response(value)
        else:
            error_messages = serializer.errors
            error_list = list(serializer.errors)
            error_message = list(serializer.errors[error_list[0]])[0]
            error = {"status": "failure", "reason": error_message }
            return Response((error), status=status.HTTP_400_BAD_REQUEST)

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            all_products = Product.objects.all()
            cart  = Cart.objects.create()
            cart.products.set(all_products)
            for i in range(len(all_products)):
                UserProduct.objects.create(product = all_products[i])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_messages = serializer.errors
            error_list = list(serializer.errors)
            error_message = list(serializer.errors[error_list[0]])[0]
            error = {"status": "failure", "reason": error_message }
            return Response((error), status=status.HTTP_400_BAD_REQUEST)

# User = get_user_model()
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # user = self.get_object(pk)
        user = User.objects.get(id = pk)
        return Response({"first_name":user.first_name,"last_name":user.last_name,"username":user.username,"email":user.email})

class BuyerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BuyerRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CartAdd(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class UserCart(APIView):
    queryset = Cart.objects.all()
    serializer_class = CartProductSerializer

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartProductSerializer(cart)
        products = []
        total_amount = 0
        for i in range(len(serializer.data['products'])):
            dic = {}
            product = Product.objects.get(name = serializer.data['products'][i]['name'])
            all_product_objects = UserProduct.objects.filter(product = product.product_id)
            user_product_id = all_product_objects[int(pk)-1].id
            user_product = UserProduct.objects.get(id = user_product_id)
            if user_product.buy_quantity != 0:
                price = product.sell_price
                total_price = price*user_product.buy_quantity
                total_amount += total_price
                dic = {"name" : serializer.data['products'][i]['name'], "quantity" : user_product.buy_quantity, "price/quantity" : price,  "total_price" : total_price}
                products.append(dic)
        return Response(({"id":serializer.data['id'],"products":products,"total_amount":total_amount}))
        # return Response((serializer.data))

class AddToCart(APIView):
    queryset = Cart.objects.all()
    serializer_class = CartProductSerializer

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartProductSerializer(cart)
        products = []
        total_amount = 0
        for i in range(len(serializer.data['products'])):
            dic = {}
            product = Product.objects.get(name = serializer.data['products'][i]['name'])
            all_product_objects = UserProduct.objects.filter(product = product.product_id)
            user_product_id = all_product_objects[int(pk)-1].id
            user_product = UserProduct.objects.get(id = user_product_id)
            if user_product.buy_quantity != 0:
                price = product.sell_price
                total_price = price*user_product.buy_quantity
                total_amount += total_price
                dic = {"name" : serializer.data['products'][i]['name'], "quantity" : user_product.buy_quantity, "price/quantity" : price,  "total_price" : total_price}
                products.append(dic)
        return Response(({"id":serializer.data['id'],"products":products,"total_amount":total_amount}))
        # return Response((serializer.data))

    def put(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartProductSerializer(cart,data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response((serializer.data))
            products = []
            total_amount = 0
            for i in range(len(serializer.data['products'])):
                dic = {}
                product = Product.objects.get(name = serializer.data['products'][i]['name'])
                all_product_objects = UserProduct.objects.filter(product = product.product_id)
                user_product_id = all_product_objects[int(pk)-1].id
                user_product = UserProduct.objects.get(id = user_product_id)
                if user_product.buy_quantity != 0:
                    price = product.sell_price
                    total_price = price*user_product.buy_quantity
                    total_amount += total_price
                    dic = {"name" : serializer.data['products'][i]['name'], "quantity" : user_product.buy_quantity, "price/quantity" : price,  "total_price" : total_price}
                    products.append(dic)
            return Response(({"id":serializer.data['id'],"products":products,"total_amount":total_amount}))
        else:
            error_messages = serializer.errors
            error_list = list(serializer.errors)
            error_message = list(serializer.errors[error_list[0]])[0]
            error = {"status": "failure", "reason": error_message }
            return Response((error), status=status.HTTP_400_BAD_REQUEST)

# class CartCheckout(APIView):
#     queryset = Cart.objects.all()
#     # serializer_class = CartProductSerializer
#
#     def get_object(self, pk):
#         try:
#             return Cart.objects.get(pk=pk)
#         except Cart.DoesNotExist:
#             raise Http404
#
#     # def get(self, request, pk, format=None):
#     #     cart = self.get_object(pk)
#     #     serializer = CartProductSerializer(cart)
#     #     products = []
#     #     total_amount = 0
#     #     for i in range(len(serializer.data['products'])):
#     #         dic = {}
#     #         product = Product.objects.get(name = serializer.data['products'][i]['name'])
#     #         all_product_objects = UserProduct.objects.filter(product = product.product_id)
#     #         user_product_id = all_product_objects[int(pk)-1].id
#     #         user_product = UserProduct.objects.get(id = user_product_id)
#     #         if user_product.buy_quantity != 0:
#     #             price = product.sell_price
#     #             total_price = price*user_product.buy_quantity
#     #             total_amount += total_price
#     #             dic = {"name" : serializer.data['products'][i]['name'], "quantity" : user_product.buy_quantity, "price/quantity" : price,  "total_price" : total_price}
#     #             products.append(dic)
#     #     return Response(({"id":serializer.data['id'],"products":products,"total_amount":total_amount}))
#         # return Response((serializer.data))
#
#     def put(self, request, pk, format=None):
#         cart = self.get_object(pk)
#         # ordered_products = self.get(request,pk)
#         serializer = CartCheckoutSerializer(cart,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # if len(ordered_products.data['products']) != 0:
#             #     print(ordered_products.data)
#             #     # print(ordered_products.data)
#             #     cart = Cart.objects.get(id = pk)
#             #     order = Orders.objects.create(cart = cart)#,address=serializer.data['address'],phone_no=serializer.data['phone_no'])
#             #     products = []
#             #     for i in range(len(ordered_products.data['products'])):
#             #         products.append(ordered_products.data['products'][i]['name'])
#             #
#             #     for i in range(len(products)):
#             #         product = Product.objects.get(name = products[i])
#             #         order.product.add(product)
#             #
#             #     order.save()
#             return Response({"status" : "updated"})
#             # else:
#             #     error = {"status": "failure", "reason": "first fill something in your cart"}
#             #     return Response((error), status=status.HTTP_400_BAD_REQUEST)
#         else:
#             error_messages = serializer.errors
#             error_list = list(serializer.errors)
#             error_message = list(serializer.errors[error_list[0]])[0]
#             error = {"status": "failure", "reason": "first fill something in your cart"}
#             return Response((error), status=status.HTTP_400_BAD_REQUEST)
class CartCheckout(APIView):
    queryset = Cart.objects.all()
    serializer_class = CartProductSerializer

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartProductSerializer(cart)
        products = []
        total_amount = 0
        for i in range(len(serializer.data['products'])):
            dic = {}
            product = Product.objects.get(name = serializer.data['products'][i]['name'])
            all_product_objects = UserProduct.objects.filter(product = product.product_id)
            user_product_id = all_product_objects[int(pk)-1].id
            user_product = UserProduct.objects.get(id = user_product_id)
            if user_product.buy_quantity != 0:
                price = product.sell_price
                total_price = price*user_product.buy_quantity
                total_amount += total_price
                dic = {"name" : serializer.data['products'][i]['name'], "quantity" : user_product.buy_quantity, "price/quantity" : price,  "total_price" : total_price}
                products.append(dic)
        return Response(({"id":serializer.data['id'],"products":products,"total_amount":total_amount,"address":"","phone_no":""}))
        # return Response((serializer.data))

    def put(self, request, pk, format=None):
        cart = self.get_object(pk)
        ordered_products = self.get(request,pk)
        length = len(ordered_products.data['products'])
        # print(ordered_products.data)
        serializer = CartCheckoutSerializer(cart,data=request.data)
        if serializer.is_valid() and length > 0:
            serializer.save()
            cart = Cart.objects.get(id = pk)
            order = Orders.objects.create(cart = cart)
            products = []
            for i in range(len(ordered_products.data['products'])):
                products.append(ordered_products.data['products'][i]['name'])

            for i in range(len(products)):
                product = Product.objects.get(name = products[i])
                order.product.add(product)
            order.save()
            return Response({"status" : "updated"})
        elif length == 0:
            error = {"status": "failure", "reason": "Your cart is empty!!" }
            return Response((error), status=status.HTTP_400_BAD_REQUEST)
        else:
            # error_messages = serializer.errors
            # error_list = list(serializer.errors)
            # error_message = list(serializer.errors[error_list[0]])[0]
            error = {"status": "failure", "reason": "1 or more fields are missing" }
            return Response((error), status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()
class OrderSummary(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CartProductSerializer(user)
        orders = []

        all_orders = Orders.objects.all()
        cart = Cart.objects.get(id = pk)
        all_user_orders = Orders.objects.filter(cart = cart)
        for i in range(len(all_user_orders)):
            order_id = all_user_orders[i].id
            dic = {"order_id":order_id}
            orders.append(dic)

        return Response({"orders":orders})
UserProduct.objects.create
class RemoveProduct(generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk, product_id, format=None):
        cart = self.get_object(pk)
        serializer = CartProductSerializer(cart)
        product_names = []
        product = Product.objects.get(product_id = product_id)
        name = product.name
        for i in range(len(serializer.data['products'])):
            product_names.append(serializer.data['products'][i]['name'])
        user_products = UserProduct.objects.filter(product = product)
        user_product = user_products[pk-1]
        if user_product.buy_quantity > 0:
            product.quantity += user_product.buy_quantity
            user_product.buy_quantity = 0
            user_product.save()
            product.save()
            return Response({"status":"removed"})
        return Response(({"status":"failure","reason":"this product is not in your cart !!"}))


# class OrderSummary(APIView):
#
#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = CartProductSerializer(user)
#         orders = []
#
#         all_orders = Orders.objects.all()
#         cart = Cart.objects.get(id = pk)
#         all_user_orders = Orders.objects.filter(cart = cart)
#         for i in range(len(all_user_orders)):
#             order_id = all_user_orders[i].id
#             dic = {"order_id":order_id}
#             orders.append(dic)
#
#         return Response({"orders":orders})

class RateProduct(APIView):
    serializer_class = RateProductSerializer
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, product_id, format=None):
        cart = self.get_object(pk)
        serializer = RateProductSerializer(cart)
        product = Product.objects.get(product_id = product_id)
        all_user_products = UserProduct.objects.filter(product = product)
        return Response({"rating":all_user_products[pk-1].rating})

    def put(self, request, pk, product_id, format=None):
        cart = self.get_object(pk)
        all_orders = Orders.objects.all()
        is_there = False
        product = Product.objects.get(product_id = product_id)
        cart = Cart.objects.get(id = pk)
        all_orders = Orders.objects.filter(cart = cart)
        for i in range(len(all_orders)):
            if (all_orders[i].product.filter(product_id = product_id).exists()):
                is_there = True
                break
        serializer = RateProductSerializer(cart,data=request.data)
        if serializer.is_valid() and is_there == True:
            serializer.save()
            all_user_products = UserProduct.objects.filter(product = product)
            rating_product = all_user_products[pk-1]
            rating_product.rating = serializer.data['rating']
            rating_product.save()
            return Response(serializer.data)
        elif serializer.is_valid() and is_there == False:
            return Response({"status":"failure","reason":"you haven't purchased this product"})
        else:
            error_messages = serializer.errors
            error_list = list(serializer.errors)
            error_message = list(serializer.errors[error_list[0]])[0]
            error = {"status": "failure", "reason": error_message }
            return Response((error), status=status.HTTP_400_BAD_REQUEST)


# class UserLogin(APIView):

def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"username":username})
        # Redirect to a success page.
        # ...
    else:
        return Response({"error":"error"})
        # Return an 'invalid login' error message.
        # ...


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
