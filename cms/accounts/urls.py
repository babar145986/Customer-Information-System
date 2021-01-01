from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('customer/', views.customer, name = "customer"),
    path('customer_view/<str:pk_test>/', views.customer_view, name="customer_view"),
    path('product/', views.product, name = "product"),
    path('create_order/', views.create_order, name = 'create_order'),
    path('update_order/<str:pk_test>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk_test>/', views.delete_order, name='delete_order'),
    path('register/', views.register, name='register'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    path('userPage/', views.userPage, name='userPage'),
]
