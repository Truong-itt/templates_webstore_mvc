from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from .models import *
import json
# su dung mau dki cua django 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        #xu li truong hop nguoi dung chua thuc hienj login vao 
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.order_items.all()
        cartItems = order.get_cart_item
        user_not_login  ="hidden"
    else :
        items = []
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_not_login  =""
    categories = Category.objects.filter(is_sub=False)
    products  = Product.objects.all()
    context = {'categories':categories,'products': products, 'cartItems':cartItems,'user_not_login':user_not_login}
    return render(request,'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_item
        items = order.order_items.all()
        user_not_login  ="hidden"
    else :
        items = []
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_not_login  =""
    categories = Category.objects.filter(is_sub=False)

    context={'items': items,'order': order, 'cartItems':cartItems,'user_not_login':user_not_login,'categories':categories}
    return render(request,'app/cart.html',context)  

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_item
        items = order.order_items.all()
        user_not_login  ="hidden"

    else :
        items = []
        cartItems = order['get_cart_item']
        order = {'get_cart_item':0,'get_cart_total':0}
        user_not_login  =""

    context={'items': items,'order': order,'cartItems':cartItems,'user_not_login':user_not_login}
    return render(request,'app/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id= productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added',safe=False)

def registry(request):
    form = CreateUserForm()
    # thuc hien kiem tra requests cua nguoi dung xem hop le hay chua
    if request.method == 'POST':   #nguoi dugn bam nut gui di kiem tra  
        form = CreateUserForm(request.POST)
        if form.is_valid(): #kiem tra thoa dieu kien hay khong
            form.save()
            
            return redirect('login')

    else:
        form = CreateUserForm()
    categories = Category.objects.filter(is_sub=False)

    context = {'form': form,'categories':categories}
    return render(request, 'app/registry.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        # redirect dung dde quay ve web 
        return redirect('home')
    if request.method == 'POST':   #nguoi dugn bam nut gui di kiem tra  
        username =  request.POST.get('username')
        password =  request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'User or password incorrect')
    categories = Category.objects.filter(is_sub=False)

    context = {'categories':categories}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    # context = {}
    logout(request)
    return redirect('login')

def search(request):
    if request.method == 'POST': 
        searched = request.POST['searched'] #lay ra ten san pham nguoi dung muon tim
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.order_items.all()
        cartItems = order.get_cart_item
    else :
        items = []
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
    products  = Product.objects.all()
    categories = Category.objects.filter(is_sub=False)

    # context = {'products': products, 'cartItems':cartItems}
    context = {'searched':searched,'keys':keys,'products': products, 'cartItems':cartItems,'categories':categories}
    return render(request, 'app/search.html', context)

from django.shortcuts import render

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category_slug = request.GET.get('category', '')

    products = Product.objects.all()  # Truy vấn mặc định

    if active_category_slug:
        # Lọc sản phẩm dựa trên slug của danh mục được chọn
        products = Product.objects.filter(category__slug=active_category_slug)

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category_slug,
    }
    return render(request, 'app/category.html', context)

def view(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_item
        items = order.order_items.all()
        user_not_login  ="hidden"
    else :
        items = []
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_not_login  =""
    categories = Category.objects.filter(is_sub=False)
    #lay id tu nguoi dung bam vao qua phuogn thuc get 
    id = request.GET.get('id')
    #lay ra dung theo san pham
    products = Product.objects.filter(id=id)
    context={'products':products,
             'items': items,
             'order': order, 
             'cartItems':cartItems,
             'user_not_login':user_not_login,
             'categories':categories}
    return render(request,'app/view.html',context)
