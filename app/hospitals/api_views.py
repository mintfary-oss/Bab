from django.db.models import Q
from rest_framework import generics, permissions

from .models import Hospital, HospitalReview
from .serializers import HospitalReviewSerializer, HospitalSerializer


class HospitalListAPIView(generics.ListAPIView):  # type: ignore[type-arg]
    serializer_class = HospitalSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):  # type: ignore[override]
        qs = Hospital.objects.filter(is_active=True)
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(address__icontains=q))
        r = self.request.GET.get("region", "").strip()
        if r:
            qs = qs.filter(region__icontains=r)
        return qs.order_by("-rating_avg")


class HospitalDetailAPIView(generics.RetrieveAPIView):  # type: ignore[type-arg]
    serializer_class = HospitalSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Hospital.objects.filter(is_active=True)


class HospitalReviewListCreateAPIView(generics.ListCreateAPIView):  # type: ignore[type-arg]
    serializer_class = HospitalReviewSerializer

    def get_queryset(self):  # type: ignore[override]
        return HospitalReview.objects.filter(hospital_id=self.kwargs["hospital_id"])

    def perform_create(self, s):
        s.save(author=self.request.user, hospital_id=self.kwargs["hospital_id"])
