import os
from typing import Any
from django.conf import settings
from rest_framework import generics,parsers,permissions,status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MediaFile
from .serializers import MediaFileSerializer,MediaUploadSerializer
from .utils import create_image_thumbnail,create_video_thumbnail,get_image_dimensions,validate_uploaded_file
class MediaUploadAPIView(APIView):
    parser_classes=[parsers.MultiPartParser,parsers.FormParser];permission_classes=[permissions.IsAuthenticated]
    def post(self,request:Request)->Response:
        s=MediaUploadSerializer(data=request.data);s.is_valid(raise_exception=True)
        d:dict[str,Any]=s.validated_data  # type: ignore[assignment]
        uf,mt=d["file"],d["media_type"]
        try: validate_uploaded_file(uf,mt)
        except Exception as e: return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        wi,hi=(None,None)
        if mt in("image","gif"): wi,hi=get_image_dimensions(uf)
        m=MediaFile.objects.create(owner=request.user,file=uf,media_type=mt,original_name=uf.name or"",mime_type=uf.content_type or"",file_size=uf.size or 0,width=wi,height=hi)
        tp=os.path.join(settings.MEDIA_ROOT,"thumbnails",f"thumb_{m.pk}.jpg")
        if mt in("image","gif") and create_image_thumbnail(m.file.path,tp): m.thumbnail=f"thumbnails/thumb_{m.pk}.jpg";m.save(update_fields=["thumbnail"])
        elif mt=="video" and create_video_thumbnail(m.file.path,tp): m.thumbnail=f"thumbnails/thumb_{m.pk}.jpg";m.save(update_fields=["thumbnail"])
        return Response(MediaFileSerializer(m,context={"request":request}).data,status=status.HTTP_201_CREATED)
class MyMediaListAPIView(generics.ListAPIView):  # type: ignore[type-arg]
    serializer_class=MediaFileSerializer
    def get_queryset(self):  # type: ignore[override]
        qs=MediaFile.objects.filter(owner=self.request.user);t=self.request.GET.get("type")
        return qs.filter(media_type=t) if t else qs
class MediaDeleteAPIView(generics.DestroyAPIView):  # type: ignore[type-arg]
    serializer_class=MediaFileSerializer
    def get_queryset(self):  # type: ignore[override]
        return MediaFile.objects.filter(owner=self.request.user)
