from django_filters import rest_framework as filters
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import News, Tag, Like, View
from .serializers import NewsSerializer, LikeSerializer, UserSerializer
from rest_framework import status
from django.db.models import Count
from .permissions import IsAdminUser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer




class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# Filter class for News
class NewsFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__name',  # Filter by tag names
        to_field_name='name',     # Match tags by their name
        queryset=Tag.objects.all()
    )

    class Meta:
        model = News
        fields = ['tags']  # Add more fields if needed

# View to list and create news articles with filtering
class NewsListCreateView(generics.ListCreateAPIView):
    """
    Handles both listing news and creating news.
    - Listing: Available to all users.
    - Creating: Restricted to admin users only.
    """
    queryset = News.objects.annotate(total_views=Count('views')).order_by('-created_at')
    serializer_class = NewsSerializer
    filter_backends = [filters.DjangoFilterBackend]  # Enable filtering
    filterset_class = NewsFilter  # Use the NewsFilter class

    def get_permissions(self):
       
        if self.request.method == 'POST':
            return [IsAdminUser()]  # Only admins can create news
        return [permissions.IsAuthenticatedOrReadOnly()]  # Read access for others

    def perform_create(self, serializer):
        serializer.save()

class NewsRetrieveDeleteView(generics.RetrieveDestroyAPIView):
   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = News.objects.annotate(total_views=Count('views'))  # Track view count
    serializer_class = NewsSerializer

    def get_permissions(self):
        """
        Returns different permissions based on the HTTP method:
        - GET (retrieve): Anyone can read (authenticated or read-only access).
        - DELETE (destroy): Only admins can delete news.
        """
        if self.request.method == "DELETE":
            return [IsAdminUser()]  # Only admins can delete news
        return [permissions.IsAuthenticatedOrReadOnly()]  # Read access for others

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a news article and tracks user views.
        """
        instance = self.get_object()
        user = request.user

        # Track views only for authenticated users
        if user.is_authenticated:
            View.objects.get_or_create(news=instance, user=user)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# View to fetch news articles with infinite scrolling
class NewsInfiniteScrollView(generics.ListAPIView):
    serializer_class = NewsSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = NewsFilter

    def get_queryset(self):
        offset = int(self.request.query_params.get('offset', 0))
        limit = 3
        return News.objects.annotate(total_views=Count('views')).order_by('-created_at')[offset:offset + limit]
    
class LikeNewsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        like_value = request.data.get('like', True)

        # Check if the user has already liked/disliked the news
        like, created = Like.objects.get_or_create(user=request.user, news=news)
        if not created:
            like.like = like_value
            like.save()
        else:
            like.like = like_value
            like.save()

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_200_OK)