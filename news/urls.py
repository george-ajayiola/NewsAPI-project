from django.urls import path
from .views import NewsListCreateView, NewsRetrieveDeleteView, LikeNewsView

urlpatterns = [
    path('news',NewsListCreateView.as_view(),name='news_list'),
    path('news/<int:pk>',NewsRetrieveDeleteView.as_view(),name='news_retrieve'),
    path('news/<int:news_id>/like/', LikeNewsView.as_view(), name='like-news'),
]