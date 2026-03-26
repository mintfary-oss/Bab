from rest_framework import generics,status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pregnancy
from .serializers import PregnancySerializer
from .weekly_data import get_week_info
class PregnancyListCreateAPIView(generics.ListCreateAPIView):  # type: ignore[type-arg]
    serializer_class=PregnancySerializer
    def get_queryset(self):  # type: ignore[override]
        return Pregnancy.objects.filter(user=self.request.user)
    def perform_create(self,s): s.save(user=self.request.user)
class PregnancyDetailAPIView(generics.RetrieveUpdateAPIView):  # type: ignore[type-arg]
    serializer_class=PregnancySerializer
    def get_queryset(self):  # type: ignore[override]
        return Pregnancy.objects.filter(user=self.request.user)
class WeekInfoAPIView(APIView):
    def get(self,request:Request,pk:int,week_num:int)->Response:
        info=get_week_info(week_num)
        if not info: return Response({"error":"Вне диапазона"},status=status.HTTP_404_NOT_FOUND)
        return Response({"week":week_num,**info})
