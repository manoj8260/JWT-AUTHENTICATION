import random
from django.core.mail import EmailMessage
from .models import User , OneTimePassword
from  django.conf import settings
def generateotp():
    otp =''
    for i in range(6):
     otp += str(random.randint(1,9))
    return otp
    
    
def send_code_to_user(email):
    subject = 'One time passcode for Email verification'
    user = User.objects.get(email =email)
    from_email =  'kumarmanoj8260910@gmail.com'
    otp = generateotp()
    messaage = f'thanks {user.first_name} for sign up verified your email using passcode-{otp}'
    to_email = user.email
    
    OneTimePassword.objects.create(
        user = user , code = otp
    )
    send_email = EmailMessage(subject = subject,body = messaage , from_email=from_email ,to=[to_email])
    send_email.send(fail_silently=True)
    
    
    
    