from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, UserListView,
    CreatePostView, PostListView, PostDetailView,
    CommentListCreateView, CommentDetailView
)

urlpatterns = [
    # Authentication
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Protected endpoints
    path('users/', UserListView.as_view(), name='user-list'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', CreatePostView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
