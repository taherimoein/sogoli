# Generated by Django 3.2.6 on 2021-08-20 19:12

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('mobile', models.CharField(db_index=True, max_length=11, unique=True, verbose_name='شماره موبایل')),
                ('first_name', models.CharField(db_index=True, max_length=50, verbose_name='نام')),
                ('last_name', models.CharField(db_index=True, max_length=150, verbose_name='نام خانوادگی')),
                ('profile', models.ImageField(default='static/images/default/default-profile.jpg', upload_to='media/images/profile/', verbose_name='پروفایل')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('following_count', models.PositiveIntegerField(default=0, verbose_name='تعداد آرایشگاه های دنبال شده')),
                ('orders_count', models.PositiveIntegerField(default=0, verbose_name='تعداد سفارشات')),
                ('superuser', models.BooleanField(default=False, verbose_name='وضعیت مدیرکل')),
                ('staff', models.BooleanField(default=False, verbose_name='وضعیت کارمند')),
                ('active', models.BooleanField(default=True, verbose_name='وضعیت فعالیت')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت کاربر')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی کاربر')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ('id', 'create_date'),
            },
        ),
        migrations.CreateModel(
            name='BeautyShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, unique=True, verbose_name='عنوان')),
                ('profile', models.ImageField(upload_to='media/images/beautyshop/', verbose_name='پروفایل')),
                ('address', models.TextField(null=True, verbose_name='آدرس')),
                ('rate', models.PositiveSmallIntegerField(default=0, verbose_name='امتیاز')),
                ('following_count', models.PositiveIntegerField(default=0, verbose_name='تعداد افراد دنبال کننده')),
                ('post_count', models.PositiveIntegerField(default=0, verbose_name='تعداد پست دنبال کننده')),
                ('orders_count', models.PositiveIntegerField(default=0, verbose_name='تعداد سفارشات')),
                ('publish', models.BooleanField(default=True, verbose_name='وضعیت انتشار')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت سالن زیبایی')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی سالن زیبایی')),
            ],
            options={
                'verbose_name': 'سالن زیبایی',
                'verbose_name_plural': 'سالن هایی زیبایی',
                'ordering': ('id', 'create_date'),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='عنوان')),
                ('image', models.ImageField(upload_to='media/images/service/', verbose_name='عکس')),
                ('publish', models.BooleanField(default=True, verbose_name='وضعیت انتشار')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت خدمت')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی خدمت')),
            ],
            options={
                'verbose_name': 'خدمت',
                'verbose_name_plural': 'خدمات',
                'ordering': ('id', 'create_date'),
            },
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')),
                ('validation_code', models.CharField(default=main.models.create_validation_code(6), max_length=6, verbose_name='کد فعال سازی')),
                ('createdatetime', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/images/post/', verbose_name='عکس')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('user_liked', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), blank=True, null=True, size=None, verbose_name='کاربران لایک کرده')),
                ('like_count', models.PositiveIntegerField(default=0, verbose_name='تعداد لایک')),
                ('publish', models.BooleanField(default=True, verbose_name='وضعیت انتشار')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت پست')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی پست')),
                ('fk_beautyshop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_beautyshop', to='main.beautyshop', verbose_name='سالن زیبایی')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست ها',
                'ordering': ('id', 'create_date'),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField(default=0, verbose_name='مجموع قیمت')),
                ('payment_status', models.BooleanField(default=False, verbose_name='وضعیت پرداخت')),
                ('publish', models.BooleanField(default=True, verbose_name='وضعیت انتشار')),
                ('reservation_date', models.DateTimeField(null=True, verbose_name='تاریخ رزرو سفارش')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت سفارش')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی سفارش')),
                ('fk_beautyshop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_beautyshop', to='main.beautyshop', verbose_name='سالن زیبایی')),
                ('fk_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_user', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارشات',
                'ordering': ('id', 'order_date'),
            },
        ),
        migrations.AddField(
            model_name='user',
            name='beautyshop_following',
            field=models.ManyToManyField(blank=True, related_name='user_beautyshop_following', to='main.BeautyShop', verbose_name='آرایشگاه های دنبال شده'),
        ),
    ]
