from django.urls import path
from .views import UserRegister , VerifyUserEmail,UserLoginView,TestAuthenticatedView
urlpatterns= [
    path('register/',UserRegister.as_view()) , 
    path('verify-email/',VerifyUserEmail.as_view()),
    path('login/',UserLoginView.as_view()),
    path('test-token/',TestAuthenticatedView.as_view()),
]