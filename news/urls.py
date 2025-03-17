from django.urls import path
from .views import NewsListCreateView, NewsRetrieveDeleteView, LikeNewsView, NewsInfiniteScrollView

urlpatterns = [
    path('news',NewsListCreateView.as_view(),name='news_list'),
    path('news/<int:pk>',NewsRetrieveDeleteView.as_view(),name='news_retrieve'),
    path('news/<int:news_id>/like/', LikeNewsView.as_view(), name='like-news'),
    path('news/infinite', NewsInfiniteScrollView.as_view(), name='infinite-news'),

]