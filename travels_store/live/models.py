from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Post(models.Model):
    """Модель поста"""
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель комментария"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_data = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['-created_data']

    def __str__(self):
        return self.text
