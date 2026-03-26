from django.contrib.auth import get_user_model
from django.db.models import Q,QuerySet
from django.http import HttpRequest,HttpResponse
from django.shortcuts import render
from chat.models import Group
from hospitals.models import Hospital
from posts.models import Post
User=get_user_model()
def search_view(request:HttpRequest)->HttpResponse:
    q=request.GET.get("q","").strip();st=request.GET.get("type","all")
    results:dict[str,QuerySet]={"posts":Post.objects.none(),"users":User.objects.none(),"hospitals":Hospital.objects.none(),"groups":Group.objects.none()}  # type: ignore[type-arg]
    if q and len(q)>=2:
        if st in("all","posts"): results["posts"]=Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q),status=Post.Status.PUBLISHED,visibility=Post.Visibility.PUBLIC).select_related("author")[:20]
        if st in("all","users"): results["users"]=User.objects.filter(Q(username__icontains=q)|Q(first_name__icontains=q),is_active=True)[:20]
        if st in("all","hospitals"): results["hospitals"]=Hospital.objects.filter(Q(name__icontains=q)|Q(address__icontains=q)|Q(region__icontains=q),is_active=True)[:20]
        if st in("all","groups"): results["groups"]=Group.objects.filter(Q(title__icontains=q),privacy=Group.Privacy.PUBLIC)[:20]
    return render(request,"search_app/results.html",{"query":q,"search_type":st,"results":results,"total":sum(qs.count() for qs in results.values())})
