import re
from django.db import models
from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
class UserManager(BaseUserManager):
  def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
      now = timezone.now()
      if not username:
          raise ValueError(_('The given username must be set'))
      email = self.normalize_email(email)
      user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user
  def create_user(self, username, email=None, password=None, **extra_fields):
      return self._create_user(username, email, password, False, False, **extra_fields)
  def create_superuser(self, username, email, password, **extra_fields):
      user=self._create_user(username, email, password, True, True, **extra_fields)
      user.is_active=True
      user.save(using=self._db)
      return user

class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(_('username'), max_length=15, unique=True, help_text=_('Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters'), validators=[ validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))])
  first_name = models.CharField(_('first name'), max_length=30)
  last_name = models.CharField(_('last name'), max_length=30)
  org_name = models.CharField(_('organization name'), max_length=100, null=True, blank=True)
  email = models.EmailField(_('email address'), max_length=255, unique=True)
  is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
  is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))

  is_public = models.BooleanField(_('is public'), default = True, help_text=("Set to true if the site is public accessible."))
  
  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['org_name', 'username']

  objects = UserManager()

  class Meta:
      verbose_name = _('user')
      verbose_name_plural = _('users') 

class Contact(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)  
  email = models.EmailField(_('email address'), max_length=255, unique=True)
  phone = models.CharField(_('phone number'), max_length=20, null=True, blank=True)
  instagram = models.CharField(_('instagram username'), max_length=30, null=True, blank=True)
  facebook = models.CharField(_('facebook username'), max_length=30, null=True, blank=True)

  class Meta:
    verbose_name = _('contact')
    verbose_name_plural = _('contacts')

class Action(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(_('title'), max_length=100)
  image = models.ImageField(_('image'), upload_to='action_images/', null=True, blank=True)
  attachments = models.FileField(_('attachments'), upload_to='action_attachments/', null=True, blank=True)
  description = models.TextField(_('description'), null=True, blank=True)
  day = models.IntegerField(_('day'), validators=[MinValueValidator(1), MaxValueValidator(31)])
  month = models.IntegerField(_('month'), validators=[MinValueValidator(1), MaxValueValidator(12)])
  year = models.IntegerField(_('year'), validators=[MinValueValidator(1900), MaxValueValidator(9999)])

  class Meta:
    verbose_name = _('action')
    verbose_name_plural = _('actions')


class DonationsPage(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(_('name'), max_length=100)
  description = models.TextField(_('description'), null=True, blank=True)
  pix = models.CharField(_('pix'), max_length=100, null=True, blank=True)

  class Meta:
    verbose_name = _('donations page')
    verbose_name_plural = _('donations pages')
