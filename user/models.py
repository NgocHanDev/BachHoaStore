from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password=None):
        if not phone_number:
            raise ValueError('Vui lòng nhập số điện thoại!')

        if not email:
            raise ValueError('Vui lòng nhập email!')
        
        user = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email),
            full_name = full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(
            phone_number=phone_number,
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login =  models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']
    
    objects = MyUserManager()
    
    def __str__(self):
        return self.phone_number + "-" + self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True