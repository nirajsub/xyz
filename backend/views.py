from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *

class MyTokenObtainPairView(TokenObtainPairView):
    permissions_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = HotelRegisterSerializer

class CustomerRegisterView(generics.CreateAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerRegisterSerializer

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class HotelHome(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        mainuser = MainUser.objects.get(user=request.user)
        customer = CustomerHotelRegister.objects.filter(hotel=mainuser)
        privilage , created = Privilage.objects.get_or_create(user=mainuser, saved=False)
        serializer = CustomerHotelRegisterSerializer(customer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchCustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        mainuser = MainUser.objects.get(user=request.user)
        customer = CustomerHotelRegister.objects.filter(hotel=mainuser)
        serializer = CustomerHotelRegisterSerializer(customer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllCustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        mainuser = MainUser.objects.get(user=request.user)
        customer = CustomerHotelRegister.objects.filter(hotel=mainuser)
        privilage = Privilage.objects.get(user=mainuser)
        serializer = CustomerHotelRegisterSerializer(customer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerRegisterApi(APIView):
    def post(self, request, *args, **kwargs):
        mainuser = MainUser.objects.get(user = request.user)
        data = {
            'name' : request.data.get('name'),
            'email' : request.data.get('email'),
            'phone_number' : request.data.get('phone_number'),
            'hotel' : mainuser.id
        }
        serializer = CustomerHotelRegisterSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return CustomerHotelRegister.objects.get(id=pk)
        except CustomerRecord.DoesNotExist:
            return None
    def get(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(user=self.request.user)
        customer = self.get_object(pk)
        curecord = CustomerRecord.objects.filter(user=customer, hotel=customer.hotel)
        serializer = CustomerRecordSerializer(curecord, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditCustomerAmount(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return CustomerRecord.objects.get(id=pk)
        except CustomerRecord.DoesNotExist:
            return None
    def put(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(user=self.request.user)
        curecord = CustomerRecord.objects.get(id=pk)
        data = {
            'amount': request.data.get('amount'),
        }
        serializer = CustomerRecordSerializer(instance = curecord, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PutAmountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return CustomerHotelRegister.objects.get(id=pk)
        except CustomerHotelRegister.DoesNotExist:
            return None
    def put(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(user=request.user)
        customer = CustomerHotelRegister.objects.get(id=pk, hotel=mainuser)
        data = {
            'amount':request.data.get('amount'),
            'user':pk,
            'hotel':mainuser.id
        }
        serializer = CustomerRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerCheckinView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(user=self.request.user)
        customer = CustomerHotelRegister.objects.get(id=pk, hotel=mainuser)
        serializer = CustomerHotelRegisterSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SetPrivilageMethod(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(user=self.request.user)
        privilage = Privilage.objects.get(id=pk, user=mainuser, saved=False)
        data = {
            'visit': request.data.get('visit'),
            'purchase': request.data.get('purchase')
        }
        serializer = SetPrivilageMethodSerializer(instance = privilage, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetVisitPrivilageMethod(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(user=self.request.user)
        privilage = Privilage.objects.get(id=pk, user=mainuser, saved=False, visit=True)
        data = {
            'silver_target_visit': request.data.get('silver_target_visit'),
            'silver_offer': request.data.get('silver_offer'),
            'gold_target_visit': request.data.get('gold_target_visit'),
            'gold_offer': request.data.get('gold_offer'),
            'diamond_target_visit': request.data.get('diamond_target_visit'),
            'diamond_offer': request.data.get('diamond_offer'),
        }
        serializer = SetVisitPrivilageSerializer(instance = privilage, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetPurchasePrivilageMethod(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(user=self.request.user)
        privilage = Privilage.objects.get(id=pk, user=mainuser, saved=False, purchase=True)
        data = {
            'silver_target_purchase': request.data.get('silver_target_purchase'),
            'silver_offer': request.data.get('silver_offer'),
            'gold_target_purchase': request.data.get('gold_target_purchase'),
            'gold_offer': request.data.get('gold_offer'),
            'diamond_target_purchase': request.data.get('diamond_target_purchase'),
            'diamond_offer': request.data.get('diamond_offer'),
        }
        serializer = SetPurchasePrivilageSerializer(instance = privilage, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PrivilageCustomerList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        mainuser = MainUser.objects.get(user=self.request.user)
        privilage = Privilage.objects.get(user=mainuser)
        customer = CustomerHotelRegister.objects.filter(hotel=mainuser)
        serializer = PrivilageCustomerSerializer(customer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
class CustomerHome(generics.ListAPIView):
    queryset = MainUser.objects.all().order_by('id')
    serializer_class = HotelSerializer

class CustomerCheckinToHotel(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(id=pk)
        customer = CustomerUser.objects.get(user=self.request.user)
        customerhotel = CustomerHotelRegister.objects.filter(user=customer, hotel=mainuser)
        serializer = CustomerUserSerializer(customer, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, pk, *args, **kwargs):
        mainuser = MainUser.objects.get(id=pk)
        customer = CustomerUser.objects.get(user=self.request.user)
        customerhotel = CustomerHotelRegister.objects.filter(user=customer, hotel=mainuser)
        if request.method == "POST":
            if CustomerHotelRegister.objects.filter(user=customer, hotel=mainuser).exists():
                pass
            else:
                customer = CustomerHotelRegister.objects.create(user=customer, hotel=mainuser, name=customer.name, email=customer.user.email, phone_number=customer.phone_number)
        serializer = HotelSerializer(mainuser)
        return Response(serializer.data, status=status.HTTP_200_OK)