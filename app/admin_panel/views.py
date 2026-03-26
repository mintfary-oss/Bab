import os,subprocess
from django.conf import settings
from django.contrib import messages as dm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse,HttpRequest,HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from .models import AdminActionLog,Report
@staff_member_required  # type: ignore[arg-type]
def moderation_dashboard_view(request:HttpRequest)->HttpResponse:
    pending=Report.objects.filter(status=Report.Status.PENDING)[:50]
    backups:list[dict[str,object]]=[]
    bd=getattr(settings,"BACKUP_DIR","")
    if bd and os.path.isdir(bd):
        for f in sorted(os.listdir(bd),reverse=True):
            if f.endswith(".gz"): backups.append({"name":f,"size_mb":round(os.path.getsize(os.path.join(bd,f))/1048576,2)})
    return render(request,"admin_panel/dashboard.html",{"pending_reports":pending,"pending_count":pending.count(),"backups":backups})
@staff_member_required  # type: ignore[arg-type]
def report_detail_view(request:HttpRequest,report_id:int)->HttpResponse:
    report=get_object_or_404(Report,pk=report_id)
    if request.method=="POST":
        action=request.POST.get("action");notes=request.POST.get("admin_notes","")
        if action=="resolve": report.status=Report.Status.RESOLVED
        elif action=="reject": report.status=Report.Status.REJECTED
        report.admin_notes=notes;report.reviewed_by=request.user;report.save()
        AdminActionLog.objects.create(admin_user=request.user,action_type=AdminActionLog.ActionType.RESOLVE_REPORT,description=f"Жалоба #{report.pk}: {action}",target_type="report",target_id=report.pk)
        return redirect("admin_panel:dashboard")
    return render(request,"admin_panel/report_detail.html",{"report":report})
@staff_member_required  # type: ignore[arg-type]
def backup_create_view(request:HttpRequest)->HttpResponse:
    bd=getattr(settings,"BACKUP_DIR","")
    if not bd: dm.error(request,"BACKUP_DIR не настроен.");return redirect("admin_panel:dashboard")
    os.makedirs(bd,exist_ok=True)
    from django.utils import timezone
    ts=timezone.now().strftime("%Y%m%d_%H%M%S");db=settings.DATABASES["default"]
    df=os.path.join(bd,f"db_{ts}.sql.gz")
    try:
        env=os.environ.copy();env["PGPASSWORD"]=str(db["PASSWORD"])
        cmd=["pg_dump","-h",str(db["HOST"]),"-p",str(db["PORT"]),"-U",str(db["USER"]),str(db["NAME"])]
        with open(df,"wb") as f:
            dp=subprocess.Popen(cmd,stdout=subprocess.PIPE,env=env)
            gp=subprocess.Popen(["gzip"],stdin=dp.stdout,stdout=f)
            if dp.stdout: dp.stdout.close()
            gp.communicate(timeout=300)
        dm.success(request,f"Бэкап: {os.path.basename(df)}")
    except Exception as e: dm.error(request,f"Ошибка: {e}")
    return redirect("admin_panel:dashboard")
@staff_member_required  # type: ignore[arg-type]
def backup_download_view(request:HttpRequest,filename:str)->HttpResponse|FileResponse:
    bd=getattr(settings,"BACKUP_DIR","");safe=os.path.basename(filename);fp=os.path.join(bd,safe)
    if not os.path.isfile(fp) or not safe.endswith(".gz"): dm.error(request,"Не найден.");return redirect("admin_panel:dashboard")
    return FileResponse(open(fp,"rb"),as_attachment=True,filename=safe)  # noqa: SIM115
