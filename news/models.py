from django.db import models
from django.contrib.auth.models import User

# Tag model to categorize news articles
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# News model to store news articles
class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    pictures = models.CharField(max_length=500, blank=True, null=True)  # Cloudinary URL
    tags = models.ManyToManyField(Tag, related_name='news')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Property to calculate total likes
    @property
    def total_likes(self):
        return self.likes.filter(like=True).count()

    # Property to calculate total dislikes
    @property
    def total_dislikes(self):
        return self.likes.filter(like=False).count()

    # Property to calculate total views
    @property
    def view_count(self):
        return self.views.count()

# Like model to track user likes/dislikes for news articles
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=True)  # True for like, False for dislike

    class Meta:
        unique_together = ('user', 'news')  # Ensure a user can only like/dislike a news item once

    def __str__(self):
        return f"{self.user.username} {'liked' if self.like else 'disliked'} {self.news.title}"

# View model to track news views (no anonymous users)
class View(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Only authenticated users
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news')  # Ensure a user can only view a news item once

    def __str__(self):
        return f"{self.news.title} viewed by {self.user.username}"