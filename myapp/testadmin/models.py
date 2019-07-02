
from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser)
from django.contrib.auth import get_user_model

# User = get_user_model()

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user_obj = self.model(
            email=self.normalize_email(email),
        )

        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user_obj = self.create_user(
            email,
            password=password,
        )
        user_obj.staff = True
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user_obj= self.create_user(
            email,
            password=password,
        )
        user_obj.staff = True
        user_obj.admin = True
        user_obj.save(using=self._db)
        return user_obj

# hook in the New Manager to our Model
# class User(AbstractBaseUser): # from step 2
    

class User(AbstractBaseUser):
    objects = UserManager()
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

class Profile(models.Model):
    user_obj=models.OneToOneField(get_user_model())
	
		

class GuestEmail(models.Model):
	Email = models.EmailField()
	active= models.BooleanField(default=True)
	update= models.DateTimeField(auto_now=True)
	timestamp=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email
