from django.shortcuts import redirect, render, get_object_or_404
from .forms import CustomerRegisterForm, CustomerProfileForm
from django.views import View
from django.contrib import messages
from .models import Customer,Product,Cart,Payment,Order
from django.db.models import Count
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django import template
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
from datetime import datetime
from django.conf import settings
from urllib.parse import quote
import momoapi
import uuid
import requests
from momoapi.client import Client
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def home(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"store/index.html",locals())


class CustomerRegisterView(View):    
    def get(self,request):
        form=CustomerRegisterForm()
        return render(request,'store/register.html',locals())
    def post(self,request):
        form=CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Chúc mừng! Đắng ký thành công')
            return redirect('register')
        return render(request,'store/register.html',locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'store/profile.html',locals())
    def post(self,request):
        try:
            customer = Customer.objects.get(user=request.user)
            messages.error(request, 'Thông tin đã nhập rồi')
            return redirect('profile')
        except Customer.DoesNotExist:
            pass
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name_customer=form.cleaned_data['name_customer']
            phone=form.cleaned_data['phone']
            address=form.cleaned_data['address']
            reg=Customer(user=user,name_customer=name_customer,phone=phone,address=address)
            reg.save()
            messages.success(request,'Chúc mừng! Lưu thông tin thành công.')
        return render(request,'store/profile.html',locals())
    
def updateprofilecus(request):
    customer_profile = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Chúc mừng! Cập nhật thông tin thành công.')
    else:
        form = CustomerProfileForm(instance=customer_profile)
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'store/updateprofilecus.html',locals())  
    
class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('name_product')
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'store/category.html',locals())
    def post(self,request,val):
        return render(request,'store/updateprofile.html',locals())
    
class CategoryDetail(View):
    def get(self,request,val):
        product=Product.objects.filter(name_product=val)
        title=Product.objects.filter(category=product[0].category).values('name_product')
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) 
        return render(request,'store/category.html',locals())
        


class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'store/productdetail.html',locals())
    
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id_product=product_id)
    Cart(user=user,product=product).save()
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return redirect('/cart')
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0 
    for p in cart:
        value=p.quantity * p.product.selling_price
        amount=amount+value
    totalamount= amount
    formatted_amount = "{:,.0f} ".format(amount)
    formatted_totalamount = "{:,.0f} ".format(totalamount)
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'store/addtocart.html',locals())

def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        user=request.user
        cart= Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value= p.quantity * p.product.selling_price
            amount=amount+value
            
        totalamount= amount 
        formatted_amount = "{:,.0f} VNĐ".format(amount)
        formatted_totalamount = "{:,.0f} VNĐ".format(totalamount)
        data={
            'quantity':c.quantity,
            'amount':formatted_amount,
            'totalamount':formatted_totalamount
        }
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return JsonResponse(data)
    
def remove_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart= Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value=p.quantity *p.product.selling_price
            amount=amount+value
        totalamount= amount 
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        
        return redirect('/cart')
    
def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        user=request.user
        cart= Cart.objects.filter(user=user)
        amount = 0
       
        for p in cart:
            value= p.quantity * p.product.selling_price
            amount=amount+value
        totalamount= amount
        formatted_amount = "{:,.0f} VNĐ".format(amount)
        formatted_totalamount = "{:,.0f} VNĐ".format(totalamount)
        data={
            'quantity':c.quantity,
            'amount':formatted_amount,
            'totalamount':formatted_totalamount
        }
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return JsonResponse(data)
    
class checkout(View):
    def get(self,request):
        customer_profile = Customer.objects.get(user=request.user)
        if request.method == 'POST':
            form = CustomerProfileForm(request.POST, instance=customer_profile)
        else:
            form = CustomerProfileForm(instance=customer_profile)
        cart= Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart:
            value= p.quantity * p.product.selling_price
            amount=amount+value
        totalamount= amount
        formatted_amount = "{:,.0f} ".format(amount)
        formatted_totalamount = "{:,.0f} ".format(totalamount)
        totalitem=0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'store/checkout.html',locals())    
    def post(self,request):
        customer_profile = Customer.objects.get(user=request.user)
        cart= Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart:
            value= p.quantity * p.product.selling_price
            amount= amount+value
        totalamount= amount
        endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
        partnerCode = "MOMO"
        accessKey = "F8BBA842ECF85"
        secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        orderInfo = "Thanh toán với MoMo"
        redirectUrl = "http://127.0.0.1:8000/"
        ipnUrl = "http://127.0.0.1:8000/"
        amountmomo = str(totalamount)
        orderId = str(uuid.uuid4())
        requestId = str(uuid.uuid4())
        requestType = "payWithMethod"
        extraData = ""
        # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
        # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
        # &requestType=$requestType
        rawSignature = "accessKey=" + accessKey + "&amount=" + str(amountmomo) + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType 
    
        # signature
        h = hmac.new(bytes(secretKey, 'utf-8'), bytes(rawSignature, 'utf-8'), hashlib.sha256)
        signature = h.hexdigest()
        data = {
            'partnerCode': partnerCode,
            'partnerName': "Test",
            'storeId': "MomoTestStore",
            'requestId': requestId,
            'amount': str(amountmomo),
            'orderId': orderId,
            'orderInfo': orderInfo,
            'redirectUrl': redirectUrl,
            'ipnUrl': ipnUrl,
            'extraData': extraData,
            'requestType': requestType,
            'signature': signature,
         
            
        }
        data = json.dumps(data)
        clen = len(data)
        response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})
        payment=Payment(
                user=request.user,
                amount=amount,
                payment_order_id=orderId,
                payment_status='Đã thanh toán',
        )
        payment_trans_id = request.GET.get('payment_trans_id')
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            return HttpResponse('Không tìm thấy thông tin khách hàng.')

        try:
            payments = Payment.objects.filter(payment_trans_id=payment_trans_id)
        except Payment.DoesNotExist:
            return HttpResponse('Không tìm thấy thông tin thanh toán.')
        payment.paid = True
        payment.payment_trans_id = payment_trans_id
        payment.save()
        cart = Cart.objects.filter(user=user)
        for c in cart:
            try:
            # Tạo đối tượng Order và lưu vào cơ sở dữ liệu
                order = Order.objects.create(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment)
            except Exception as e:
                return HttpResponse(f'Lỗi khi tạo đơn hàng: {str(e)}')
        # Xóa sản phẩm từ giỏ hàng sau khi tạo đối tượng Order
            c.delete()  
        if response.status_code == 200:
            response_data = response.json()
            pay_url = response_data.get("payUrl")
            if pay_url:
                return redirect(pay_url)
            else:
                print("Không tìm thấy URL thanh toán trong phản hồi từ Momo.")
        else:
            print(f"Lỗi {response.status_code}: {response.text}")
      
        return redirect("orders")
    
def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(name_product__icontains=query))
   
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'store/search.html',locals())

def orders(request):
    order_place=Order.objects.filter(user=request.user)
    return render(request,'store/orders.html',locals())

def product_detail(request, id_product):
    product = get_object_or_404(Product, pk=id_product)
    return render(request, 'product_detail.html', {'product': product})