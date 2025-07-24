from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserRegisterSerializers(serializers.ModelSerializer) : 
    password = serializers.CharField(max_length =68 , min_length = 6 ,write_only = True)
    password1 = serializers.CharField(max_length =68 , min_length = 6 ,write_only = True)
    
    class Meta :
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password1']
        
    def validate(self, attrs):
        password1 = attrs.get('password','')
        password2 = attrs.get('password1','')
        if password1 != password2 :
            raise serializers.ValidationError('password does not match')
        return attrs
    
    
    def create(self, validated_data):
        print(validated_data)
        validated_data.pop('password1')
        user = User.objects.create_user(
            **validated_data
        )
        return user   
 
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length =250,min_length = 6)    
    password = serializers.CharField(max_length  =68,write_only= True)  
    full_name = serializers.CharField(max_length = 255,read_only = True)
    refresh_token = serializers.CharField(max_length = 255,read_only = True)
    access_token = serializers.CharField(max_length = 255,read_only = True)
    
    
    class Meta:
        model = User
        fields= ['email','password','full_name','refresh_token' ,'access_token']
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request =self.context.get('request')
        user = authenticate(request,email = email,password =password)
        if not user :
            raise AuthenticationFailed('crendienatial does not match')
        if not user.is_verified :
            raise AuthenticationFailed('email is not verified')
        user_tokens = user.tokens()
        
        return {
            'email' :user.email ,
            'full_name' :user.full_name,
            'refresh_token' :str(user_tokens.get('refresh')),
            'access_token' : str(user_tokens.get('access'))
        }
        
        
          