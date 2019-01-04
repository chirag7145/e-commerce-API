from django.conf.urls import include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.urls import path
urlpatterns = [

    path('api/products/<int:pk>/',views.ProductDetail.as_view(),name='product_detail'),
    path('api/product/add/',views.ProductCreate.as_view(),name='create_product'),
    path('api/product/delete/<int:pk>/',views.ProductDelete.as_view(),name='delete_product'),
    path('api/product/update/<int:pk>/',views.ProductUpdate.as_view(),name='update_product'),

    path('api/user/register/',views.UserRegister.as_view(),name='register_user'),
    path('api/user/detail/<int:pk>/',views.UserDetail.as_view(),name='user_detail'),
    path('api/user/login',views.loginview,name='login_user'),

    path('api/orders/<int:pk>/', views.OrderSummary.as_view(),name='orders'),

    path('api/cart/<int:pk>/', views.UserCart.as_view(),name='user_cart'),
    path('api/cart/<int:pk>/add/', views.AddToCart.as_view(),name='add_to_cart'),
    path('api/cart/<int:pk>/checkout/', views.CartCheckout.as_view(),name='cart_checkout'),
    path('api/cart/<int:pk>/remove/<int:product_id>/', views.RemoveProduct.as_view(),name='remove_product'),
    path('api/user/<int:pk>/product/rate/<int:product_id>/', views.RateProduct.as_view(),name='rate_product'),

    ]
