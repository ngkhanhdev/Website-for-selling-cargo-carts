from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    id_customer=models.BigAutoField(primary_key=True)
    name_customer=models.CharField(max_length=200)
    phone=PhoneNumberField(region='VN')
    address=models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.id_customer:
            last_customer = Customer.objects.all().order_by('-id_customer').first()
            if last_customer:
                self.id_customer = last_customer.id_customer + 1
            else:
                self.id_customer = 1

        super(Customer, self).save(*args, **kwargs)

   

CATEGORY_CHOICES=(
  ('T-W-C','Two-wheeled cart'),
  ('F-W-C','Four-wheeled cart'),
  ('M-C-C','Multifunctional cargo cart'),
  ('F-C-C','Foldable cargo cart'),
)

class Product(models.Model):
    id_product=models.BigAutoField(primary_key=True)
    name_product=models.CharField(max_length=100)
    quantity_product=models.PositiveIntegerField(default=1)
    selling_price=models.DecimalField(max_digits=10, decimal_places=0)
    description=models.TextField()
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=6)
    product_image=models.ImageField(upload_to='product')
    
    def __str__(self):
        return self.name_product
    
    def save(self, *args, **kwargs):
        if not self.id_product:
            last_product = Product.objects.all().order_by('-id_product').first()
            if last_product:
                self.id_product = last_product.id_product + 1
            else:
                self.id_product = 1

        super(Product, self).save(*args, **kwargs)
    
    def formatted_price(self):
        return f"{self.selling_price:,.0f}"

class Cart(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    id_cart=models.BigAutoField(primary_key=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity*self.product.selling_price
    
    def save(self, *args, **kwargs):
        if not self.id_cart:
            last_cart = Cart.objects.all().order_by('-id_cart').first()
            if last_cart:
                self.id_cart = last_cart.id_cart + 1
            else:
                self.id_cart = 1

        super(Cart, self).save(*args, **kwargs)

STATUS_CHOICES=(
   
    ('Đang chờ','Đang chờ'),
    ('Đã duyệt','Đã duyệt'),
    ('Đang giao','Đang giao'),
    ('Hoàn tất','Hoàn tất'),
    ('Huỷ','Huỷ'),
)

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    payment_order_id=models.CharField(max_length=50,blank=True,null=True)
    payment_status = models.CharField(max_length=50,blank=True,null=True)
    payment_trans_id=models.CharField(max_length=100,blank=True,null=True)
    payment_date = models.DateTimeField(auto_now_add=True)  # Use a default value instead of auto_now_add
    paid=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.id:
            last_payment = Payment.objects.all().order_by('-id').first()
            if last_payment:
                self.id = last_payment.id + 1
            else:
                self.id = 1
        super(Payment, self).save(*args, **kwargs)
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,default="Đang chờ",choices=STATUS_CHOICES)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.id:
            last_order = Order.objects.all().order_by('-id').first()
            if last_order:
                self.id = last_order.id + 1
            else:
                self.id = 1
        super(Order, self).save(*args, **kwargs)
        
    def total_cost(self):
        return self.quantity * self.product.selling_price

