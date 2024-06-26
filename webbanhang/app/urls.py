from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home,name='home'),
    path('cart/', views.cart,name ='cart'),  
    path('checkout/', views.checkout,name ='checkout'),  
    path('update_item/', views.updateItem,name ='update_item'),  
    path('login/', views.loginPage,name ='login'),  
    path('registry/', views.registry,name ='registry'),  
    path('logout/', views.logoutPage,name ='logout'),  
    path('search/', views.search,name ='search'),  
    path('category/', views.category,name ='category'),  
    path('view/', views.view,name ='view'),  
]
