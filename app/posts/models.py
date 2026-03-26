from django.conf import settings
from django.db import models
from django.utils import timezone
class Tag(models.Model):
    name=models.CharField(max_length=50,unique=True);slug=models.SlugField(max_length=60,unique=True)
    class Meta: verbose_name="Тег";verbose_name_plural="Теги";ordering=["name"]
    def __str__(self): return self.name
class Post(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC="public","Публичный";FRIENDS="friends","Друзья";PRIVATE="private","Приватный"
    class Status(models.TextChoices):
        DRAFT="draft","Черновик";PUBLISHED="published","Опубликован"
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="posts")
    title=models.CharField(max_length=300);body=models.TextField()
    visibility=models.CharField(max_length=10,choices=Visibility.choices,default=Visibility.PUBLIC)
    status=models.CharField(max_length=12,choices=Status.choices,default=Status.PUBLISHED)
    tags=models.ManyToManyField(Tag,blank=True,related_name="posts")
    media_files=models.ManyToManyField("media_app.MediaFile",blank=True,related_name="posts")
    pregnancy=models.ForeignKey("pregnancy.Pregnancy",on_delete=models.SET_NULL,blank=True,null=True,related_name="posts")
    pregnancy_week=models.PositiveSmallIntegerField(blank=True,null=True)
    created_at=models.DateTimeField(default=timezone.now);updated_at=models.DateTimeField(auto_now=True)
    class Meta: verbose_name="Пост";verbose_name_plural="Посты";ordering=["-created_at"]
    def __str__(self): return self.title
    @property
    def likes_count(self): return self.likes.count()  # type: ignore[attr-defined]
    @property
    def comments_count(self): return self.comments.count()  # type: ignore[attr-defined]
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="comments")
    body=models.TextField(max_length=2000)
    parent=models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True,related_name="replies")
    created_at=models.DateTimeField(default=timezone.now)
    class Meta: ordering=["created_at"]
class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="likes")
    created_at=models.DateTimeField(default=timezone.now)
    class Meta: unique_together=[("post","user")]
