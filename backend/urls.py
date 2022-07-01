
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    # auths
    path('change_password/<str:pk>/', ChangePasswordView.as_view(), name="change_password"),
    path('login/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('login/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # customer
    path('cregister/', CustomerRegisterView.as_view(), name='cregister'),
    path('customercheckin/<str:pk>/', CustomerCheckinToHotel.as_view(), name="customercheckin"),
    path('customerhome/', CustomerHome.as_view(), name="customerhome"),

    # hptel
    path('hotelregister/', RegisterView.as_view(), name='hotelregister'),
    path('searchcustomer/', SearchCustomerView.as_view(), name="searchcustomer"),
    path('customer_checkin/<str:pk>/', CustomerCheckinView.as_view(), name="customer_checkin"),
    path('hotelhome/', HotelHome.as_view(), name='hotelhome'),
    path('detailcustomer/<str:pk>/', CustomerDetails.as_view(), name="detailcustomer"),
    path('editcustomeramount/<str:pk>/', EditCustomerAmount.as_view(), name="editcustomeramount"),
    path('enteramount/<str:pk>/', PutAmountView.as_view(), name="enteramount"),
    path('registercustomer/', CustomerRegisterApi.as_view(), name="registercustomer"),
    path('set_privilage/<str:pk>', SetPrivilageMethod.as_view(), name="set_privilage"),
    path('setvisitprivilage/<str:pk>/', SetVisitPrivilageMethod.as_view(), name="setvisitprivilage"),
    path('setpurchaseprivilage/<str:pk>/', SetPurchasePrivilageMethod.as_view(), name="setpurchaseprivilage"),
    path('privilagecustomerlist/', PrivilageCustomerList.as_view(), name="privilagecustomerlist"),
]
