from django.contrib.auth.decorators import login_required
from django.http import HttpRequest,HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .forms import CommentForm,PostForm
from .models import Like,Post
def feed_view(request:HttpRequest)->HttpResponse:
    posts=Post.objects.filter(status=Post.Status.PUBLISHED,visibility=Post.Visibility.PUBLIC).select_related("author").prefetch_related("tags")[:50]
    return render(request,"posts/feed.html",{"posts":posts})
@login_required
def post_create_view(request:HttpRequest)->HttpResponse:
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            p=form.save(commit=False);p.author=request.user;p.save();form.save_m2m()
            return redirect("posts:detail",post_id=p.pk)
    else: form=PostForm()
    return render(request,"posts/create.html",{"form":form})
@login_required
def post_edit_view(request:HttpRequest,post_id:int)->HttpResponse:
    post=get_object_or_404(Post,pk=post_id,author=request.user)
    if request.method=="POST":
        form=PostForm(request.POST,instance=post)
        if form.is_valid(): form.save();return redirect("posts:detail",post_id=post.pk)
    else: form=PostForm(instance=post)
    return render(request,"posts/edit.html",{"form":form,"post":post})
def post_detail_view(request:HttpRequest,post_id:int)->HttpResponse:
    post=get_object_or_404(Post.objects.select_related("author").prefetch_related("tags","comments__author"),pk=post_id)
    comments=post.comments.filter(parent__isnull=True).select_related("author")  # type: ignore[attr-defined]
    liked=request.user.is_authenticated and Like.objects.filter(post=post,user=request.user).exists()
    return render(request,"posts/detail.html",{"post":post,"comments":comments,"comment_form":CommentForm(),"user_liked":liked})
@login_required
@require_POST
def comment_create_view(request:HttpRequest,post_id:int)->HttpResponse:
    post=get_object_or_404(Post,pk=post_id);form=CommentForm(request.POST)
    if form.is_valid():
        c=form.save(commit=False);c.post=post;c.author=request.user
        pid=request.POST.get("parent_id")
        if pid: c.parent_id=int(pid)
        c.save()
    return redirect("posts:detail",post_id=post.pk)
@login_required
@require_POST
def like_toggle_view(request:HttpRequest,post_id:int)->HttpResponse:
    post=get_object_or_404(Post,pk=post_id)
    like,created=Like.objects.get_or_create(post=post,user=request.user)
    if not created: like.delete()
    if request.headers.get("X-Requested-With")=="XMLHttpRequest":
        return JsonResponse({"liked":created,"likes_count":post.likes.count()})  # type: ignore[attr-defined]
    return redirect("posts:detail",post_id=post.pk)
@login_required
def post_delete_view(request:HttpRequest,post_id:int)->HttpResponse:
    post=get_object_or_404(Post,pk=post_id,author=request.user)
    if request.method=="POST": post.delete();return redirect("posts:feed")
    return render(request,"posts/delete_confirm.html",{"post":post})
@login_required
def my_posts_view(request:HttpRequest)->HttpResponse:
    return render(request,"posts/my_posts.html",{"posts":Post.objects.filter(author=request.user)})
