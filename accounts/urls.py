from django.urls import path
from .views import (UserRegister , VerifyUserEmail,UserLoginView,
                    TestAuthenticatedView , PasswordResetRequestView,
                    PaswordResetConfirmView,NewPasswordView,LogoutView)
urlpatterns= [
    path('register/',UserRegister.as_view()) , 
    path('verify-email/',VerifyUserEmail.as_view()),
    path('login/',UserLoginView.as_view()),
    path('test-token/',TestAuthenticatedView.as_view()),
    path('password-reset/',PasswordResetRequestView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',PaswordResetConfirmView.as_view(),name='password-reset-confirm'),
    path('new-password/',NewPasswordView.as_view()),
    path('logout/',LogoutView.as_view())
]