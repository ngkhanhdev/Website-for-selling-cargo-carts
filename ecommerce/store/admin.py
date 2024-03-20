from django.contrib import admin
from .models import Customer,Product,Cart,Payment,Order

# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id_customer','name_customer','phone','address']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=   ['id_product','name_product','selling_price','quantity_product','category','product_image']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=   ['id_cart','user','product','quantity']    

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=   ['id','user','amount','payment_order_id','payment_date','payment_status','paid']    
    
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=   ['id','user','customer','product','quantity','ordered_date','status','payment'] 
   