from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your models here.
#change forms register dhango 
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # cac thuoc tinh co san cua dajando 
        fields = ['username', 'email', 'first_name', 'last_name','password1', 'password2']

# class Customer(models.Model):
#     user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=False)
#     name = models.CharField(max_length=200,null=True)
#     email = models.CharField(max_length=200,null=True)
#     def __str__(self):
#         return self.name

class Category(models.Model):
    #vi du san pham co man hay ngot chua cac thu hay khong
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_categorys',null=True,blank=True)
    #co phai la danh muc con hay khong
    is_sub = models.BooleanField(default=False,null=True)
    name = models.CharField(max_length=200,null=True)
    # toi uu duong dan 
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self) :
        return self.name

class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    detail = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=False)
    date_order = models.DateField(auto_now_add=True,null=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_item(self):
        orderitems = self.order_items.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False, related_name='order_items')
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=False)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=False)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.address
    
