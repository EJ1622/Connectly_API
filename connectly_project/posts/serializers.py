from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile, Post, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'posts_count', 'comments_count']
        read_only_fields = ['id']
    
    def get_posts_count(self, obj):
        return obj.posts.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'updated_at', 'comments_count']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def validate_content(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Post content must be at least 5 characters.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
    
    def validate(self, data):
        # Ensure comment belongs to existing post
        post = Post.objects.filter(id=data['post'].id).first()
        if not post:
            raise serializers.ValidationError("Post does not exist.")
        return data
    
    def validate_text(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Comment must be at least 3 characters.")
        return value
