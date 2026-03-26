from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest,HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from .models import Pregnancy,WeeklyChecklist
from .weekly_data import WEEKS_DATA,get_week_info
@login_required
def pregnancy_dashboard_view(request:HttpRequest)->HttpResponse:
    p=Pregnancy.objects.filter(user=request.user,status=Pregnancy.Status.ACTIVE).first()
    if not p: return redirect("pregnancy:create")
    w=p.current_week
    return render(request,"pregnancy/dashboard.html",{"pregnancy":p,"week":w,"week_info":get_week_info(w),"checklist":WeeklyChecklist.objects.filter(pregnancy=p,week=w)})
@login_required
def pregnancy_create_view(request:HttpRequest)->HttpResponse:
    if request.method=="POST":
        dd=request.POST.get("due_date")
        if dd:
            p=Pregnancy.objects.create(user=request.user,due_date=dd)
            items=[]
            for wn,info in WEEKS_DATA.items():
                for task in info["checklist"]: items.append(WeeklyChecklist(pregnancy=p,week=wn,title=task))
            WeeklyChecklist.objects.bulk_create(items)
            messages.success(request,"Трекер создан!");return redirect("pregnancy:dashboard")
    return render(request,"pregnancy/create.html")
@login_required
def week_detail_view(request:HttpRequest,week_num:int)->HttpResponse:
    p=get_object_or_404(Pregnancy,user=request.user,status=Pregnancy.Status.ACTIVE)
    wi=get_week_info(week_num)
    if not wi: return redirect("pregnancy:dashboard")
    return render(request,"pregnancy/week_detail.html",{"pregnancy":p,"week_num":week_num,"week_info":wi,"checklist":WeeklyChecklist.objects.filter(pregnancy=p,week=week_num),"is_current":p.current_week==week_num})
@login_required
def checklist_toggle_view(request:HttpRequest,item_id:int)->HttpResponse:
    item=get_object_or_404(WeeklyChecklist,pk=item_id,pregnancy__user=request.user)
    item.is_done=not item.is_done;item.save(update_fields=["is_done"])
    return redirect("pregnancy:week_detail",week_num=item.week)
@login_required
def weeks_overview_view(request:HttpRequest)->HttpResponse:
    p=get_object_or_404(Pregnancy,user=request.user,status=Pregnancy.Status.ACTIVE)
    return render(request,"pregnancy/weeks_overview.html",{"pregnancy":p,"weeks_range":list(range(1,43))})
