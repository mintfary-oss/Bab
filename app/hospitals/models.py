from django.conf import settings
from django.db import models
from django.utils import timezone
class Hospital(models.Model):
    class HospitalType(models.TextChoices):
        PUBLIC="public","Государственный";PRIVATE="private","Частный"
    name=models.CharField(max_length=300);region=models.CharField(max_length=200,db_index=True)
    city=models.CharField(max_length=200,blank=True,default="");address=models.CharField(max_length=500)
    phone=models.CharField(max_length=50,blank=True,default="");email=models.EmailField(blank=True,default="")
    website=models.URLField(blank=True,default="")
    hospital_type=models.CharField(max_length=10,choices=HospitalType.choices,default=HospitalType.PUBLIC)
    description=models.TextField(blank=True,default="");contacts=models.JSONField(default=dict,blank=True)
    working_hours=models.CharField(max_length=200,blank=True,default="");amenities=models.JSONField(default=list,blank=True)
    photos=models.ManyToManyField("media_app.MediaFile",blank=True,related_name="hospitals")
    rating_avg=models.DecimalField(max_digits=3,decimal_places=2,default=0)
    reviews_count=models.PositiveIntegerField(default=0);is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(default=timezone.now);updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-rating_avg","name"]
    def __str__(self): return f"{self.name} ({self.region})"
class HospitalReview(models.Model):
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE,related_name="reviews")
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="hospital_reviews")
    rating=models.PositiveSmallIntegerField(choices=[(i,str(i)) for i in range(1,6)])
    body=models.TextField(max_length=3000);is_recommended=models.BooleanField(default=True)
    visited=models.BooleanField(default=False);created_at=models.DateTimeField(default=timezone.now)
    class Meta: ordering=["-created_at"];unique_together=[("hospital","author")]
    def save(self,*a,**kw):
        super().save(*a,**kw)  # type: ignore[arg-type]
        from django.db.models import Avg,Count
        s=HospitalReview.objects.filter(hospital=self.hospital).aggregate(avg=Avg("rating"),cnt=Count("id"))
        self.hospital.rating_avg=s["avg"] or 0;self.hospital.reviews_count=s["cnt"] or 0
        self.hospital.save(update_fields=["rating_avg","reviews_count"])
