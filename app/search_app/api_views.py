from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions,status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.models import Group
from chat.serializers import GroupSerializer
from hospitals.models import Hospital
from hospitals.serializers import HospitalSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from users.serializers import UserSerializer
User=get_user_model()
class SearchAPIView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request:Request)->Response:
        q=request.GET.get("q","").strip()
        if not q or len(q)<2: return Response({"error":"Минимум 2 символа"},status=status.HTTP_400_BAD_REQUEST)
        data:dict[str,list[object]]={}
        data["posts"]=PostSerializer(Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q),status=Post.Status.PUBLISHED,visibility=Post.Visibility.PUBLIC)[:20],many=True).data  # type: ignore[assignment]
        data["users"]=UserSerializer(User.objects.filter(Q(username__icontains=q),is_active=True)[:20],many=True).data  # type: ignore[assignment]
        data["hospitals"]=HospitalSerializer(Hospital.objects.filter(Q(name__icontains=q),is_active=True)[:20],many=True).data  # type: ignore[assignment]
        data["groups"]=GroupSerializer(Group.objects.filter(Q(title__icontains=q),privacy=Group.Privacy.PUBLIC)[:20],many=True).data  # type: ignore[assignment]
        return Response({"query":q,"results":data})
