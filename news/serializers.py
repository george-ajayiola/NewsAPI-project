from rest_framework import serializers
from django.contrib.auth.models import User
from .models import News, Tag, Like, View
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)
        # Add custom fields to the token
        token["is_staff"] = user.is_staff
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
# Serializer for Tag model
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# Serializer for News model
class NewsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'text', 'pictures', 'tags', 'created_at',
            'total_likes', 'total_dislikes', 'view_count'
        ]

    def get_total_likes(self, obj):
        return obj.total_likes

    def get_total_dislikes(self, obj):
        return obj.total_dislikes

    def get_view_count(self, obj):
        # Use the annotated total_views field
        return obj.total_views if hasattr(obj, 'total_views') else obj.view_count

# Serializer for Like model
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'news', 'like']

# Serializer for View model
class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ['id', 'news', 'user', 'viewed_at']