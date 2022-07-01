
from django.shortcuts import render, redirect
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import *

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token

class HotelRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    org_name = serializers.CharField(required=True)
    class Meta:
        model = MainUser
        fields = ['username', 'email', 'password', 'password2', 'org_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        mainuser = MainUser.objects.create(
            user=user,
            org_name=validated_data['org_name'],
        )
        mainuser.save()
        return user

class CustomerRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(required=True)
    phone_number = serializers.IntegerField(required=True)
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'password2', 'name', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        customer = CustomerUser.objects.create(
            user=user,
            name=validated_data['name'],
            phone_number=validated_data['phone_number']
        )
        customer.save()
        return user

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password field didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "old password is not correct"})
        return value
        
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'
    
class PrivilageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilage
        fields = '__all__'
        
class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'
    
class CustomerHotelRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerHotelRegister
        fields = '__all__'
    
class PrivilageCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerHotelRegister
        exclude = ['user']

class CustomerRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRecord
        fields = '__all__'

class SearchCustomerHotelRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerHotelRegister
        fields = '__all__'

class SetPrivilageMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilage
        fields = ['visit', 'purchase']

class SetVisitPrivilageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilage
        fields = ['silver_target_visit', 'silver_offer', 'gold_target_visit', 'gold_offer', 'diamond_target_visit', 'diamond_offer']

class SetPurchasePrivilageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilage
        fields = ['silver_target_purchase', 'silver_offer', 'gold_target_purchase', 'gold_offer', 'diamond_target_purchase', 'diamond_offer']
    
