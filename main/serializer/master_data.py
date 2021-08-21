from rest_framework.serializers import ModelSerializer, SerializerMethodField
from main.models import BeautyShop, Post, User

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