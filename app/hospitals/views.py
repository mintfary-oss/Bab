from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Hospital, HospitalReview


def hospital_list_view(request: HttpRequest) -> HttpResponse:
    qs = Hospital.objects.filter(is_active=True)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(address__icontains=q) | Q(city__icontains=q))
    r = request.GET.get("region", "").strip()
    if r:
        qs = qs.filter(region__icontains=r)
    t = request.GET.get("type", "").strip()
    if t:
        qs = qs.filter(hospital_type=t)
    regions = (
        Hospital.objects.filter(is_active=True)
        .values_list("region", flat=True)
        .distinct()
        .order_by("region")
    )
    return render(
        request,
        "hospitals/list.html",
        {
            "hospitals": qs[:100],
            "regions": regions,
            "query": q,
            "selected_region": r,
            "selected_type": t,
        },
    )


def hospital_detail_view(request: HttpRequest, hospital_id: int) -> HttpResponse:
    h = get_object_or_404(
        Hospital.objects.prefetch_related("photos", "reviews__author"),
        pk=hospital_id,
        is_active=True,
    )
    reviews = h.reviews.select_related("author")[:20]  # type: ignore[attr-defined]
    ur = (
        HospitalReview.objects.filter(hospital=h, author=request.user).first()
        if request.user.is_authenticated
        else None
    )
    return render(
        request, "hospitals/detail.html", {"hospital": h, "reviews": reviews, "user_review": ur}
    )


@login_required
def hospital_review_view(request: HttpRequest, hospital_id: int) -> HttpResponse:
    h = get_object_or_404(Hospital, pk=hospital_id, is_active=True)
    if request.method == "POST":
        rt, bd = request.POST.get("rating"), request.POST.get("body", "").strip()
        if rt and bd:
            HospitalReview.objects.update_or_create(
                hospital=h,
                author=request.user,
                defaults={
                    "rating": int(rt),
                    "body": bd,
                    "is_recommended": request.POST.get("is_recommended") == "on",
                    "visited": request.POST.get("visited") == "on",
                },
            )
            messages.success(request, "Отзыв сохранён!")
    return redirect("hospitals:detail", hospital_id=h.pk)
