from django.db import models
from django.contrib.auth.models import   PermissionsMixin,AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from accounts.managers import  UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractBaseUser , PermissionsMixin):
    """
    Custom user model that extends the default Django user model.
    """
    email = models.EmailField(_('email address'), unique=True,max_length=255)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('is_active') , default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    
    
    def has_perm(self, perm, obj=None):
        """
        Checks if the user has a specific permission.
        """
        return self.is_superuser or self.user_permissions.filter(codename=perm).exists()
    def has_module_perms(self, app_label):
        """
        Checks if the user has permissions for a specific app.
        """
        return self.is_superuser or self.user_permissions.filter(content_type__app_label=app_label).exists()
    
    @property
    def full_name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.last_name}".strip()
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),  
             'access': str(refresh.access_token)
        }
        
        


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class OneTimePassword(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6,unique=True)
    
    
    def __str__(self):
        return f'{self.user.first_name} - passcode'