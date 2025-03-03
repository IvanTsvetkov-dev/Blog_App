from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft' # Пара значение-метка
        PUBLISHED = 'PB', 'Published'
        
        
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) # При создании объекта, будет присвоена дата создания
    updated = models.DateTimeField(auto_now=True) # При каждом измении объекта, будет изменено и поле Update
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    objects = models.Manager() # Менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер
    
    # Сортировка постов по убыванию даты и времени публикации
    class Meta:
        ordering = ['-publish']
        
        indexes = [
            models.Index(fields=['-publish'])
        ]
    def __str__(self):
        return self.title