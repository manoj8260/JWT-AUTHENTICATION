from django.shortcuts import render
from .models import User ,OneTimePassword
from .serializers import UserRegisterSerializers ,LoginSerializer
from  rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from rest_framework.permissions import IsAuthenticated

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




