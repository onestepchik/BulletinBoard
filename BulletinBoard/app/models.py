from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.
# class User(User):
#     rate = models.IntegerField(default=0)
#     def __str__(self):
#         return self.username
    
class Category(models.Model):
    categoryName = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.categoryName

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length = 255, default = "Facilis consequatur eligendi")
    content =  models.TextField(default = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Facilis consequatur eligendi quisquam doloremque vero ex debitis veritatis placeat unde animi laborum sapiente illo possimus, commodi dignissimos obcaecati illum maiores corporis.")
    image = models.ImageField(upload_to='images', default='images/default.jpg')
    def __str__(self):
        return self.title
    
    def preview(self):
        return self.content[:124] + "..."
    
    @property
    def number_of_comments(self):
        return Response.objects.filter(post=self).count()
    
    @property
    def getComments(self):
        return Response.objects.filter(post=self)

    
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField(default='')
    date_create = models.DateTimeField(auto_now_add=True)
    isAccepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField(auto_now_add=True)
    
