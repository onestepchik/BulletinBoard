from django.contrib import admin
from .models import Category, Post, Response
from django.db import models
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.get_fields() if field.related_model == models.OneToOneRel]

class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_create', 'title', 'content', 'category']
    list_filter = ('user', 'category')
    search_fields = ('user', 'date_create', 'title', 'content', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName',]
    list_filter = ('categoryName',)
    search_fields = ('categoryName',)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'message', 'isAccepted']
    list_filter = ('user', 'isAccepted')
    search_fields = ('user', 'post', 'message', 'isAccepted')
    
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Response, ResponseAdmin)
