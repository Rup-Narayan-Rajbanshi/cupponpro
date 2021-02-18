from django.contrib import admin
from articleapp.models.news import NewsArticle
from articleapp.models.blogs import Blog
# Register your models here.

admin.site.register(NewsArticle)
admin.site.register(Blog)