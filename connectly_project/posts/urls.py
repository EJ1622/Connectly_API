from django.urls import path
from .views import (
    UserListCreateView, UserRetrieveUpdateDestroyView,
    PostListCreateView, PostRetrieveUpdateDestroyView
)

urlpatterns = [
    # Users
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    
    # Posts
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
]
