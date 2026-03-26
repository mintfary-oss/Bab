import math
from datetime import date,timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
class Pregnancy(models.Model):
    class Status(models.TextChoices):
        ACTIVE="active","Активная";CLOSED="closed","Завершена"
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="pregnancies")
    due_date=models.DateField("ПДР")
    conception_date=models.DateField(blank=True,null=True)
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.ACTIVE)
    notes=models.TextField(blank=True,default="")
    created_at=models.DateTimeField(default=timezone.now)
    class Meta: ordering=["-created_at"]
    def __str__(self): return f"Беременность {self.user} — ПДР {self.due_date}"
    @property
    def current_week(self):
        lmp=self.due_date-timedelta(days=280);return max(1,min(42,math.ceil((date.today()-lmp).days/7)))
    @property
    def current_day(self):
        lmp=self.due_date-timedelta(days=280);return max(0,(date.today()-lmp).days)
    @property
    def days_remaining(self): return max(0,(self.due_date-date.today()).days)
    @property
    def progress_percent(self): return round(min(100.0,max(0.0,((280-self.days_remaining)/280)*100)),1)
    @property
    def trimester(self):
        w=self.current_week
        if w<=13: return 1
        if w<=27: return 2
        return 3
class WeeklyChecklist(models.Model):
    pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE,related_name="checklists")
    week=models.PositiveSmallIntegerField();title=models.CharField(max_length=300)
    is_done=models.BooleanField(default=False);created_at=models.DateTimeField(default=timezone.now)
    class Meta: ordering=["week","pk"]
    def __str__(self): return f"[{'+' if self.is_done else '-'}] Нед.{self.week}: {self.title}"
