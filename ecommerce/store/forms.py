from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer



class LoginCustomerForm(AuthenticationForm):
    username=UsernameField(label='Tên đăng nhập',widget=forms.TextInput(attrs={'autofocus': 'True' , 'class':'form-control'}))
    password= forms.CharField(label='Mật khẩu',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    
class CustomerRegisterForm(UserCreationForm):
    username=forms.CharField(label='Tên Đăng nhập',widget=forms.TextInput(attrs={'autofocus': 'True' , 'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1= forms.CharField(label='Mật khẩu',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(label='Nhập lại mật khẩu',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields=['email','username','password1','password2']
        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label='Mật khẩu cũ', widget=forms.PasswordInput(attrs={'autofocus': 'True' ,'autocomplete':'current-password', 'class':'form-control'}))
    new_password1=forms.CharField(label='Mật khẩu mới', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2=forms.CharField(label='Nhập lại mật khẩu mới', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    
    
class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=  Customer
        fields=['name_customer','phone','address']
        widgets={
            'name_customer': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.NumberInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'name_customer': 'Tên khách hàng', 
            'phone': 'Số điện thoại',  
            'address': 'Địa chỉ', 
        }
class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label='Mật khẩu mới', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2=forms.CharField(label='Nhập lại mật khẩu mới', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))