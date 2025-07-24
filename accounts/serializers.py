from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
# for password reset
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import  smart_bytes ,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email

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
        
class PaswordResetRequestSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    
    
    class Meta:
        model = User
        fields =['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('password-reset-confirm',kwargs={'uidb64' : uidb64,'token':token})
            abs_link = f'http://{site_domain}{relative_link}'
            email_body = f'To  follow bellow the link reset your password \n {abs_link} '
            
            data ={
                'email_body' :email_body,
                'email_subject' : 'password reset email',
                'to_email': user.email
            }
            send_normal_email(data)                
        return   super().validate(attrs)         
          
class NewPasswordSerializers(serializers.Serializer):
    new_password =  serializers.CharField(max_length =68,min_length =6,write_only=True)         
    confirm_password =  serializers.CharField(max_length =68,min_length =6,write_only=True)  
    uidb64 = serializers.CharField(write_only= True)       
    token = serializers.CharField(write_only= True)   
    
    
    # class Meta:
    #     fields = ['new_password','confirm_password','uidb64','token']   
        
    def validate(self, attrs):
        try :
            new_password = attrs.get('new_password')
            confirm_password = attrs.get('confirm_password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = uid)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('reset link has expired or invalid',401)
            if new_password != confirm_password:
                raise AuthenticationFailed('password does not match')
            user.set_password(new_password)
            user.save()
            return user
        except Exception as e :
            raise AuthenticationFailed('reset link has expired or invalid')