from django.contrib import admin
from .models import Hospital,HospitalReview
class RInline(admin.TabularInline):  # type: ignore[type-arg]
    model=HospitalReview;extra=0
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    inlines=[RInline];list_display=["name","region","hospital_type","rating_avg","is_active"];list_filter=["region","hospital_type"];filter_horizontal=["photos"]
@admin.register(HospitalReview)
class HRAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display=["hospital","author","rating","created_at"]
