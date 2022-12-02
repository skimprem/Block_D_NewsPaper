from django.contrib import admin
from .models import Category, Post



class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'post_type', 'pub_time')
    list_filter = ('categories', 'post_type')
    search_fields = ('title', 'text')

admin.site.register(Category)
admin.site.register(Post, PostAdmin)