from django.contrib import admin
from .models import Pregnancy,WeeklyChecklist
class WCInline(admin.TabularInline):  # type: ignore[type-arg]
    model=WeeklyChecklist;extra=0
@admin.register(Pregnancy)
class PregnancyAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    inlines=[WCInline];list_display=["user","due_date","status","current_week","progress_percent","created_at"]
