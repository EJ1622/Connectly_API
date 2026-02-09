from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from singletons.logger_singleton import LoggerSingleton
from factories.post_factory import PostFactory

logger = LoggerSingleton().get_logger()

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['user_id'] = user.id
        return token
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Safe way to add user info
        if request.user.is_authenticated:
            response.data['user'] = {
                'id': request.user.id,
                'username': request.user.username
            }
        return response

# Protected User Views
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Protected Post Views
class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating post for user: {request.user.username}")
        try:
            post = PostFactory.create_post(
                post_type=request.data['post_type'],
                title=self.request.data.get('title', self.request.data['content'][:50]),
                content=request.data.get('content', ''),
                metadata=request.data.get('metadata', {}),
                author=request.user
            )
            logger.info(f"Post created successfully: ID {post.id}")
            
            # Serialize the ACTUAL POST OBJECT, not request data
            serializer = self.get_serializer(post)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
        except ValueError as e:
            logger.error(f"Post creation failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

# Protected Comment Views  
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
