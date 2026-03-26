from rest_framework import serializers
from .models import Pregnancy,WeeklyChecklist
class PregnancySerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    current_week=serializers.ReadOnlyField();days_remaining=serializers.ReadOnlyField();progress_percent=serializers.ReadOnlyField();trimester=serializers.ReadOnlyField()
    class Meta: model=Pregnancy;fields=["id","due_date","conception_date","status","notes","current_week","days_remaining","progress_percent","trimester","created_at"]
class WeeklyChecklistSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta: model=WeeklyChecklist;fields=["id","week","title","is_done","created_at"]
