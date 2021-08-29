from rest_framework.serializers import ModelSerializer, SerializerMethodField
from main.models import BeautyShop, Post, User, Order
from django.utils import timezone
import jdatetime

# ---------------------------------------------------------------------------------------------------------------------------------

class BeautyShopSerializer(ModelSerializer):
    profile = SerializerMethodField('get_profile')
    class Meta:
        model = BeautyShop
        fields = [
            'id',
            'title',
            'profile',
            'address',
            'rate'
        ]
        read_only_fields = [
            'id',
            'title',
            'profile',
            'address',
            'rate'
        ]
    def get_profile(self, value):
        return value.profile.url


class BeautyShopDetailsSerializer(ModelSerializer):
    profile = SerializerMethodField('get_profile')
    services = SerializerMethodField('get_services')
    class Meta:
        model = BeautyShop
        fields = [
            'id',
            'title',
            'profile',
            'address',
            'services',
            'rate',
            'following_count',
            'post_count'
        ]
        read_only_fields = [
            'id',
            'title',
            'profile',
            'address',
            'services',
            'rate',
            'following_count',
            'post_count'
        ]
    def get_profile(self, value):
        return value.profile.url
    def get_services(self, value):
        return value.services['list']


class PostSerializer(ModelSerializer):
    image = SerializerMethodField('get_image')
    class Meta:
        model = Post
        fields = [
            'id',
            'image'
        ]
        read_only_fields = [
            'id',
            'image'
        ]
    def get_image(self, value):
        return value.image.url

    
class UserDetailsSerializer(ModelSerializer):
    profile = SerializerMethodField('get_profile')
    full_name = SerializerMethodField('get_full_name')
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'profile',
            'mobile',
            'email',
            'following_count',
            'orders_count'
        ]
        read_only_fields = [
            'id',
            'full_name',
            'profile',
            'mobile',
            'email',
            'following_count',
            'orders_count'
        ]
    def get_full_name(self, value):
        return value.get_fullname()
    def get_profile(self, value):
        return value.profile.url


class UserOrderSerializer(ModelSerializer):
    beautyshop = SerializerMethodField('get_beautyshop_info')
    order_date = SerializerMethodField('get_reservation_date')
    order_time = SerializerMethodField('get_reservation_time')
    services = SerializerMethodField('get_services')
    class Meta:
        model = Order
        fields = [
            'id',
            'beautyshop',
            'services',
            'total_price',
            'payment_status',
            'order_date',
            'order_time'
        ]
        read_only_fields = [
            'id',
            'beautyshop',
            'services',
            'total_price',
            'payment_status',
            'order_date',
            'order_time'
        ]
    def get_beautyshop_info(self, value):
        return {
            'id': value.fk_beautyshop.id,
            'title': value.fk_beautyshop.title,
            'address': value.fk_beautyshop.address,
            'profile': value.fk_beautyshop.profile.url
        }
    def get_reservation_time(self, value):
        return timezone.localtime(value.reservation_date).strftime('%H:%M')
    def get_reservation_date(self, value):
        # month
        month = {
            1: 'فروردین',
            2: 'اردیبهشت',
            3: 'خرداد',
            4: 'تیر',
            5: 'مرداد',
            6: 'شهریور',
            7: 'مهر',
            8: 'آبان',
            9: 'آذر',
            10: 'دی',
            11: 'بهمن',
            12: 'اسفند'
        }
        # get date to str
        gyear = value.reservation_date.year
        gmonth = value.reservation_date.month
        gday = value.reservation_date.day
        today = jdatetime.date.fromgregorian(day=gday,month=gmonth,year=gyear) 
        today_to_str = today.j_weekdays_fa[today.weekday()] + ' ' + str(today.day) + ' ' + month[today.month] + ' ' + str(today.year)
        return today_to_str
    def get_services(self, value):
        return value.services['list']


class BeautyShopOrderSerializer(ModelSerializer):
    user = SerializerMethodField('get_user_info')
    order_date = SerializerMethodField('get_reservation_date')
    order_time = SerializerMethodField('get_reservation_time')
    services = SerializerMethodField('get_services')
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'services',
            'total_price',
            'payment_status',
            'order_date',
            'order_time'
        ]
        read_only_fields = [
            'id',
            'user',
            'services',
            'total_price',
            'payment_status',
            'order_date',
            'order_time'
        ]
    def get_user_info(self, value):
        return {
            'id': value.fk_user.id,
            'fullname': value.fk_user.get_fullname(),
        }
    def get_reservation_time(self, value):
        return timezone.localtime(value.reservation_date).strftime('%H:%M')
    def get_reservation_date(self, value):
        # month
        month = {
            1: 'فروردین',
            2: 'اردیبهشت',
            3: 'خرداد',
            4: 'تیر',
            5: 'مرداد',
            6: 'شهریور',
            7: 'مهر',
            8: 'آبان',
            9: 'آذر',
            10: 'دی',
            11: 'بهمن',
            12: 'اسفند'
        }
        # get date to str
        gyear = value.reservation_date.year
        gmonth = value.reservation_date.month
        gday = value.reservation_date.day
        today = jdatetime.date.fromgregorian(day=gday,month=gmonth,year=gyear) 
        today_to_str = today.j_weekdays_fa[today.weekday()] + ' ' + str(today.day) + ' ' + month[today.month] + ' ' + str(today.year)
        return today_to_str
    def get_services(self, value):
        return value.services['list']