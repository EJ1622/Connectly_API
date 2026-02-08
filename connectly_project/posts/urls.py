from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView
)

urlpatterns = [
    # Users
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # Posts
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # Comments
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
