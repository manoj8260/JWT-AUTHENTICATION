from django.shortcuts import render
from .models import User ,OneTimePassword
from .serializers import UserRegisterSerializers ,LoginSerializer
from  rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from rest_framework.permissions import IsAuthenticated
# for password reset
from .serializers import PaswordResetRequestSerializer , NewPasswordSerializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str ,DjangoUnicodeDecodeError

# Create your views here.

class UserRegister(GenericAPIView) : 
    serializer_class  =UserRegisterSerializers
    
    def post(self,request) :
        user_data = request.data
        serializer = self.serializer_class(data = user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(serializer.data.get('email'))
            return Response(
                {
                    'data' : user,
                    'message' : f'hii  thanks for sign up '
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)    
        
class VerifyUserEmail(GenericAPIView):
    def post(self,request):
        enter_otp = request.data.get('otp')
        try:
            usercode_obj = OneTimePassword.objects.get(code = enter_otp)
            user= usercode_obj.user
            if not user.is_verified :
               user.is_verified = True
               user.save()
               return Response({
                   'message' : ' emial verified sucessfully',
            
               },status=status.HTTP_201_CREATED)
            return Response(  {'message' : 'code is alerady vefied'},status=status.HTTP_205_RESET_CONTENT)   
        
        except OneTimePassword.DoesNotExist:
            return Response(
                {
                    'message' : ' passcode  not  provided'
                } , status=status.HTTP_404_NOT_FOUND
            )    
                
class UserLoginView(GenericAPIView) : 
    serializer_class = LoginSerializer
    def post(self,request):
        serializer= self.serializer_class(data = request.data ,context ={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
           
class TestAuthenticatedView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data ={
            'message' : 'its work'
        }
        return Response(data,status=status.HTTP_200_OK)

class PasswordResetRequestView(GenericAPIView):
    serializer_class = PaswordResetRequestSerializer
    
    def post(self,request):
        seralizer = self.serializer_class(data=request.data,context = {'request':request})
        seralizer.is_valid(raise_exception=True)
        return Response(
            {
                'messgae' :'a password reset link sebd to your register email id ,check your email !'
            },status=status.HTTP_200_OK
        )
class PaswordResetConfirmView(GenericAPIView):
    def get(self,request,uidb64,token):
        try:
           uid  = smart_str(urlsafe_base64_decode(uidb64))
           user = User.objects.get(id = uid)
           if not PasswordResetTokenGenerator().check_token(user,token):
               return Response({'message' : 'token has invalid or expired'},status=status.HTTP_200_OK)
           return Response({'sucess' : True ,'message' : 'credentials is valid', 'uidb64':uidb64 ,'token' :token })
        except DjangoUnicodeDecodeError:   
            return Response({'message' : 'token has invalid or expired'},status=status.HTTP_401_UNAUTHORIZED)
        
    
class NewPasswordView(GenericAPIView):
    serializer_class =NewPasswordSerializers 
    def patch(self,request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'message' : 'password reset confirm '
        },status=status.HTTP_200_OK)
           
        


