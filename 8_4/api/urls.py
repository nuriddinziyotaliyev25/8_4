from django.urls import path
from rest_framework.response import Response

from . import views

app_name = 'api'
urlpatterns = [
    # Customer
    path('customer/list/', views.CustomerListView.as_view(), name='customer_list'),
    path('customer/<int:pk>/detail/', views.CustomerDetailView.as_view(), name='customer_detail'),

    # Category
    path('category/list/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/detail/', views.CategoryDetailView.as_view(), name='category_detail'),

    # Food
    path('food/list/', views.FoodListView.as_view(), name='food_list'),
    path('food/<slug:slug>/detail/', views.FoodDetailView.as_view(), name='food_detail'),

    # Order
    path('order/list/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:id>/detail/', views.OrderDetailView.as_view(), name='order_detail'),
]