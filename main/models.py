from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.utils.deconstruct import deconstructible
from django.db.models import JSONField
from django.db import models
import random, string

# ------------------------------------------------------------------------------------------------------------------------------------

@deconstructible
class default_json_field():
    def __call__(self):
        return {'list': []}


@deconstructible
class create_validation_code():
    def __init__(self, size):
        self.size = size

    def __call__(self):
        code = ''.join(random.choice(string.digits) for i in range(self.size))
        return code

# ------------------------------------------------------------------------------------------------------------------------------------

# Validation (اعتبار سنجی) Model   
class Validation(models.Model):
    mobile = models.CharField(verbose_name = 'شماره موبایل', max_length = 11, unique = True)
    validation_code = models.CharField(verbose_name = 'کد فعال سازی', max_length = 6, default = create_validation_code(6))
    createdatetime = models.DateTimeField(verbose_name = 'تاریخ و زمان ایجاد', auto_now_add = True)

# --------------------------------------------------------------------------------------------------------------------------------------

class UserManager(BaseUserManager):
    def create_user(self, mobile, **kwargs):
        if not mobile:
            raise ValueError("Users must have mobile")
        user = self.model(mobile = mobile, **kwargs)
        user.set_password(mobile)
        user.save()
        return user

    def create_staffuser(self, mobile, **kwargs):
        user = self.model(mobile = mobile, staff = True, **kwargs)
        user.set_password(mobile)
        user.save()
        return user

    def create_superuser(self, mobile, **kwargs):
        user = self.model(mobile = mobile, staff = True, superuser = True, **kwargs)
        user.set_password(mobile)
        user.save()
        return user

# --------------------------------------------------------------------------------------------------------------------------------------

# User (کاربر) Model
class User(AbstractBaseUser):
    mobile = models.CharField(verbose_name = 'شماره موبایل', max_length = 11, db_index = True, unique = True)
    first_name = models.CharField(verbose_name = 'نام', max_length = 50, db_index = True)
    last_name = models.CharField(verbose_name = 'نام خانوادگی', max_length = 150, db_index = True)
    profile = models.ImageField(verbose_name = 'پروفایل', upload_to = 'media/images/profile/', default = 'static/images/default/default-profile.jpg')
    email = models.EmailField(verbose_name = 'ایمیل', blank = True, null = True)
    following_count = models.PositiveIntegerField(verbose_name = 'تعداد آرایشگاه های دنبال شده', default = 0)
    orders_count = models.PositiveIntegerField(verbose_name = 'تعداد سفارشات', default = 0)
    beautyshop_following = models.ManyToManyField('BeautyShop', verbose_name = 'آرایشگاه های دنبال شده', related_name = 'user_beautyshop_following', blank = True)
    superuser = models.BooleanField(verbose_name = 'وضعیت مدیرکل', default = False)
    staff = models.BooleanField(verbose_name = 'وضعیت کارمند', default = False)
    active = models.BooleanField(verbose_name = 'وضعیت فعالیت', default = True)
    create_date = models.DateTimeField(verbose_name = 'تاریخ ثبت کاربر', auto_now_add = True)
    update_date = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی کاربر', auto_now = True)

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_staff(self):
        return self.staff

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_fullname(self):
        return ' '.join([self.first_name, self.last_name])

    class Meta:
        ordering = ('id', 'create_date')
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

# --------------------------------------------------------------------------------------------------------------------------------------

# Service (خدمت) Model
class Service(models.Model):
    title = models.CharField(verbose_name = 'عنوان', max_length = 50, db_index = True, unique = True)
    image = models.ImageField(verbose_name = 'عکس', upload_to = 'media/images/service/')
    color = models.SmallIntegerField(verbose_name = 'کد رنگ', blank = True, null = True)
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', default = True)
    create_date = models.DateTimeField(verbose_name = 'تاریخ ثبت خدمت', auto_now_add = True)
    update_date = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی خدمت', auto_now = True)

    def __str__(self):
        return '{}'.format(self.title)


    class Meta:
        ordering = ('id', 'create_date')
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمات'

# --------------------------------------------------------------------------------------------------------------------------------------

# BeautyShop (سالن زیبایی) Model
class BeautyShop(models.Model):
    title = models.CharField(verbose_name = 'عنوان', max_length = 150, db_index = True, unique = True)
    profile = models.ImageField(verbose_name = 'پروفایل', upload_to = 'media/images/beautyshop/')
    address = models.TextField(verbose_name = 'آدرس', null = True)
    rate = models.PositiveSmallIntegerField(verbose_name = 'امتیاز', default = 0)
    user_rate = JSONField(verbose_name = 'امتیاز کاربران', default = default_json_field())
    services = JSONField(verbose_name = 'خدمات', default = default_json_field())
    following_count = models.PositiveIntegerField(verbose_name = 'تعداد افراد دنبال کننده', default = 0)
    post_count = models.PositiveIntegerField(verbose_name = 'تعداد پست', default = 0)
    orders_count = models.PositiveIntegerField(verbose_name = 'تعداد سفارشات', default = 0)
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', default = True)
    create_date = models.DateTimeField(verbose_name = 'تاریخ ثبت سالن زیبایی', auto_now_add = True)
    update_date = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی سالن زیبایی', auto_now = True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('id', 'create_date')
        verbose_name = 'سالن زیبایی'
        verbose_name_plural = 'سالن هایی زیبایی'

# --------------------------------------------------------------------------------------------------------------------------------------

# Post (پست) Model
class Post(models.Model):
    image = models.ImageField(verbose_name = 'عکس', upload_to = 'media/images/post/')
    description = models.TextField(verbose_name = 'توضیحات', blank = True, null = True)
    fk_beautyshop = models.ForeignKey(BeautyShop, verbose_name = 'سالن زیبایی', related_name = 'post_beautyshop', on_delete = models.SET_NULL, null = True)
    user_liked = ArrayField(models.BigIntegerField(), verbose_name = 'کاربران لایک کرده', null = True, blank = True)
    like_count = models.PositiveIntegerField(verbose_name = 'تعداد لایک', default = 0)
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', default = True)
    create_date = models.DateTimeField(verbose_name = 'تاریخ ثبت پست', auto_now_add = True)
    update_date = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی پست', auto_now = True)

    def __str__(self):
        return '{}'.format(self.fk_beautyshop.title)

    class Meta:
        ordering = ('id', 'create_date')
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

# --------------------------------------------------------------------------------------------------------------------------------------

# Order (سفارش) Model
class Order(models.Model):
    fk_user = models.ForeignKey(User, verbose_name = 'کاربر', related_name = 'order_user', on_delete = models.SET_NULL, null = True)
    fk_beautyshop = models.ForeignKey(BeautyShop, verbose_name = 'سالن زیبایی', related_name = 'order_beautyshop', on_delete = models.SET_NULL, null = True)
    services = JSONField(verbose_name = 'خدمات خریداری شده', default = default_json_field())
    total_price = models.PositiveIntegerField(verbose_name = 'مجموع قیمت', default = 0)
    payment_status = models.BooleanField(verbose_name = 'وضعیت پرداخت', default = False)
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', default = True)
    reservation_date = models.DateTimeField(verbose_name = 'تاریخ رزرو سفارش', null = True)
    order_date = models.DateTimeField(verbose_name = 'تاریخ ثبت سفارش', auto_now_add = True)
    update_date = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی سفارش', auto_now = True)

    def __str__(self):
        return '{} - {}'.format(self.fk_beautyshop.title, self.fk_user.get_fullname())

    class Meta:
        ordering = ('id', 'order_date')
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

# --------------------------------------------------------------------------------------------------------------------------------------
