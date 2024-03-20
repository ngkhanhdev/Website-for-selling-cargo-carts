from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginCustomerForm, MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
urlpatterns=[
    path('', views.home , name='home'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('updateprofilecus/',views.updateprofilecus,name='updateprofilecus'),
    path('category/<slug:val>',views.CategoryView.as_view(),name='category'),
    path('categorydetail/<val>',views.CategoryDetail.as_view(),name='categorydetail'),
    path('productdetail/<int:pk>',views.ProductDetail.as_view(),name='productdetail'),
    path('changepassword/',auth_view.PasswordChangeView.as_view(template_name='store/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='changepassword'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('orders/',views.orders,name='orders'),
    path('search/',views.search,name='search'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    #path('momo-callback/', views.momo_callback, name='momo-callback'),
   # path('paymentdone/',views.payment_done,name='paymentdone'),
    # login and register
    path('register/', views.CustomerRegisterView.as_view(),name='register'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='store/login.html', authentication_form=LoginCustomerForm,next_page='home'), name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='home'),name='logout'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='store/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='store/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='store/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'),name='password_reset_complete'),
    
]