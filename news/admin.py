from django.contrib import admin
from .models import News, Tag, Like, View

# Register the Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Fields to display in the admin list view
    search_fields = ('name',)  # Enable search by name
    list_per_page = 20  # Number of items per page

# Register the News model
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at','view_count', 'total_likes', 'total_dislikes')
    search_fields = ('title', 'text')  # Enable search by title and text
    filter_horizontal = ('tags',)  # Better UI for many-to-many field (tags)
    list_per_page = 20

    # Custom methods to display calculated fields in the admin
    def view_count(self, obj):
        return obj.view_count
    view_count.short_description = 'Views'  # Column header in admin

    def total_likes(self, obj):
        return obj.total_likes
    total_likes.short_description = 'Likes'

    def total_dislikes(self, obj):
        return obj.total_dislikes
    total_dislikes.short_description = 'Dislikes'

# Register the Like model
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'news', 'like')
    list_filter = ('like',)  # Enable filtering by like/dislike
    search_fields = ('user__username', 'news__title')  # Enable search by username and news title
    list_per_page = 20

# Register the View model
@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'news', 'viewed_at')
    list_filter = ('viewed_at',)  # Enable filtering by viewed date
    search_fields = ('user__username', 'news__title')  # Enable search by username and news title
    list_per_page = 20