from rest_framework import generics,permissions,status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment,Like,Post
from .serializers import CommentSerializer,PostSerializer
class PostListCreateAPIView(generics.ListCreateAPIView):  # type: ignore[type-arg]
    serializer_class=PostSerializer
    def get_queryset(self):  # type: ignore[override]
        return Post.objects.filter(status=Post.Status.PUBLISHED).select_related("author")
    def perform_create(self,s): s.save(author=self.request.user)
class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):  # type: ignore[type-arg]
    serializer_class=PostSerializer;queryset=Post.objects.all()
class CommentListCreateAPIView(generics.ListCreateAPIView):  # type: ignore[type-arg]
    serializer_class=CommentSerializer
    def get_queryset(self):  # type: ignore[override]
        return Comment.objects.filter(post_id=self.kwargs["post_id"])
    def perform_create(self,s): s.save(author=self.request.user,post_id=self.kwargs["post_id"])
class LikeToggleAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request:Request,post_id:int)->Response:
        l,c=Like.objects.get_or_create(post_id=post_id,user=request.user)
        if not c: l.delete()
        return Response({"liked":c,"likes_count":Like.objects.filter(post_id=post_id).count()},status=status.HTTP_200_OK)
