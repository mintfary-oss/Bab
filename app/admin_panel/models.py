from django.conf import settings
from django.db import models
from django.utils import timezone
class Report(models.Model):
    class TargetType(models.TextChoices):
        POST="post","Пост";COMMENT="comment","Комментарий";USER="user","Пользователь";MESSAGE="message","Сообщение"
    class Status(models.TextChoices):
        PENDING="pending","На рассмотрении";RESOLVED="resolved","Решена";REJECTED="rejected","Отклонена"
    class Reason(models.TextChoices):
        SPAM="spam","Спам";ABUSE="abuse","Оскорбление";INAPPROPRIATE="inappropriate","Неприемлемый";OTHER="other","Другое"
    reporter=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="reports_filed")
    target_type=models.CharField(max_length=20,choices=TargetType.choices)
    target_id=models.PositiveIntegerField()
    reason=models.CharField(max_length=20,choices=Reason.choices,default=Reason.OTHER)
    description=models.TextField(max_length=2000,blank=True,default="")
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)
    admin_notes=models.TextField(blank=True,default="")
    reviewed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="reports_reviewed")
    created_at=models.DateTimeField(default=timezone.now);updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-created_at"]
    def __str__(self): return f"Жалоба #{self.pk}"
class AdminActionLog(models.Model):
    class ActionType(models.TextChoices):
        BLOCK_USER="block_user","Блокировка";RESOLVE_REPORT="resolve_report","Решение жалобы";OTHER="other","Другое"
    admin_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="admin_actions")
    action_type=models.CharField(max_length=20,choices=ActionType.choices)
    description=models.TextField(max_length=2000)
    target_type=models.CharField(max_length=50,blank=True,default="")
    target_id=models.PositiveIntegerField(blank=True,null=True)
    created_at=models.DateTimeField(default=timezone.now)
    class Meta: ordering=["-created_at"]
class SiteSettings(models.Model):
    site_name=models.CharField(max_length=200,default="BabyBlog")
    site_description=models.TextField(max_length=1000,default="Сообщество для беременных")
    logo=models.ImageField(upload_to="images/site/",blank=True,null=True)
    primary_color=models.CharField(max_length=7,default="#e91e8c")
    secondary_color=models.CharField(max_length=7,default="#6c757d")
    accent_color=models.CharField(max_length=7,default="#ffc107")
    background_color=models.CharField(max_length=7,default="#f8f9fa")
    footer_text=models.TextField(max_length=500,blank=True,default="")
    announcement=models.TextField(max_length=500,blank=True,default="")
    maintenance_mode=models.BooleanField(default=False)
    social_vk=models.URLField(blank=True,default="");social_telegram=models.URLField(blank=True,default="")
    meta_keywords=models.CharField(max_length=500,blank=True,default="")
    meta_description=models.CharField(max_length=300,blank=True,default="")
    max_posts_per_day=models.PositiveIntegerField(default=20)
    auto_moderate_new_users=models.BooleanField(default=False)
    banned_words=models.TextField(blank=True,default="")
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: verbose_name="Настройки сайта";verbose_name_plural="Настройки сайта"
    def __str__(self): return self.site_name
    def save(self,*a,**kw): self.pk=1;super().save(*a,**kw)  # type: ignore[arg-type]
    @classmethod
    def load(cls)->"SiteSettings":
        obj,_=cls.objects.get_or_create(pk=1);return obj
