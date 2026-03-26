from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import MediaFile


@login_required
def media_detail_view(request: HttpRequest, media_id: int) -> HttpResponse:
    return render(
        request, "media_app/detail.html", {"media": get_object_or_404(MediaFile, pk=media_id)}
    )


@login_required
def my_media_view(request: HttpRequest) -> HttpResponse:
    qs = MediaFile.objects.filter(owner=request.user)
    t = request.GET.get("type")
    if t:
        qs = qs.filter(media_type=t)
    return render(
        request,
        "media_app/my_media.html",
        {"media_files": qs, "total_size_mb": round(sum(m.file_size for m in qs) / 1048576, 1)},
    )
