from django.contrib import messages as dm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Chat, ChatMember, Friendship, Group, GroupMember, Message, Notification

User = get_user_model()


@login_required
def friends_list_view(r: HttpRequest) -> HttpResponse:
    friends = Friendship.objects.filter(
        Q(from_user=r.user, status=Friendship.Status.ACCEPTED)
        | Q(to_user=r.user, status=Friendship.Status.ACCEPTED)
    ).select_related("from_user", "to_user")
    pending = Friendship.objects.filter(
        to_user=r.user, status=Friendship.Status.PENDING
    ).select_related("from_user")
    return render(r, "chat/friends.html", {"friends": friends, "pending": pending})


@login_required
def friend_request_view(r: HttpRequest, user_id: int) -> HttpResponse:
    t = get_object_or_404(User, pk=user_id)
    if t != r.user:
        Friendship.objects.get_or_create(from_user=r.user, to_user=t)
        Notification.objects.create(
            user=t,
            notification_type=Notification.NotificationType.FRIEND_REQUEST,
            title="Запрос в друзья",
            message=f"{r.user} хочет добавить вас.",
        )
        dm.success(r, "Запрос отправлен!")
    return redirect("users:profile", user_id=user_id)


@login_required
def friend_accept_view(r: HttpRequest, friendship_id: int) -> HttpResponse:
    f = get_object_or_404(
        Friendship, pk=friendship_id, to_user=r.user, status=Friendship.Status.PENDING
    )
    f.status = Friendship.Status.ACCEPTED
    f.save(update_fields=["status"])
    return redirect("chat:friends")


@login_required
def friend_reject_view(r: HttpRequest, friendship_id: int) -> HttpResponse:
    f = get_object_or_404(Friendship, pk=friendship_id)
    if f.from_user == r.user or f.to_user == r.user:
        f.delete()
    return redirect("chat:friends")


@login_required
def chat_list_view(r: HttpRequest) -> HttpResponse:
    chats = [m.chat for m in ChatMember.objects.filter(user=r.user).select_related("chat")]
    return render(r, "chat/chat_list.html", {"chats": chats})


@login_required
def chat_detail_view(r: HttpRequest, chat_id: int) -> HttpResponse:
    chat = get_object_or_404(Chat, pk=chat_id)
    if not ChatMember.objects.filter(chat=chat, user=r.user).exists():
        return redirect("chat:list")
    return render(
        r,
        "chat/chat_detail.html",
        {
            "chat": chat,
            "messages": Message.objects.filter(chat=chat).select_related("sender")[:100],
            "members": ChatMember.objects.filter(chat=chat).select_related("user"),
        },
    )


@login_required
def send_message_view(r: HttpRequest, chat_id: int) -> HttpResponse:
    if r.method == "POST":
        body = r.POST.get("body", "").strip()
        if body:
            Message.objects.create(chat_id=chat_id, sender=r.user, body=body)
    return redirect("chat:detail", chat_id=chat_id)


@login_required
def start_chat_view(r: HttpRequest, user_id: int) -> HttpResponse:
    t = get_object_or_404(User, pk=user_id)
    my = set(ChatMember.objects.filter(user=r.user).values_list("chat_id", flat=True))
    their = set(ChatMember.objects.filter(user=t).values_list("chat_id", flat=True))
    common = Chat.objects.filter(pk__in=my & their, is_group=False).first()
    if common:
        return redirect("chat:detail", chat_id=common.pk)
    chat = Chat.objects.create(is_group=False, owner=r.user)
    ChatMember.objects.create(chat=chat, user=r.user, role=ChatMember.Role.ADMIN)
    ChatMember.objects.create(chat=chat, user=t)
    return redirect("chat:detail", chat_id=chat.pk)


@login_required
def group_list_view(r: HttpRequest) -> HttpResponse:
    return render(r, "chat/groups.html", {"public_groups": Group.objects.filter(privacy=Group.Privacy.PUBLIC)[:50], "my_groups": Group.objects.filter(group_members__user=r.user)})  # type: ignore[attr-defined]


@login_required
def group_create_view(r: HttpRequest) -> HttpResponse:
    if r.method == "POST":
        title = r.POST.get("title", "").strip()
        if title:
            g = Group.objects.create(
                owner=r.user,
                title=title,
                description=r.POST.get("description", ""),
                privacy=r.POST.get("privacy", Group.Privacy.PUBLIC),
            )
            GroupMember.objects.create(group=g, user=r.user, role=GroupMember.Role.ADMIN)
            return redirect("chat:group_detail", group_id=g.pk)
    return render(r, "chat/group_create.html")


@login_required
def group_detail_view(r: HttpRequest, group_id: int) -> HttpResponse:
    g = get_object_or_404(Group, pk=group_id)
    members = GroupMember.objects.filter(group=g).select_related("user")
    return render(
        r,
        "chat/group_detail.html",
        {"group": g, "members": members, "is_member": members.filter(user=r.user).exists()},
    )


@login_required
def group_join_view(r: HttpRequest, group_id: int) -> HttpResponse:
    GroupMember.objects.get_or_create(group_id=group_id, user=r.user)
    return redirect("chat:group_detail", group_id=group_id)


@login_required
def group_leave_view(r: HttpRequest, group_id: int) -> HttpResponse:
    GroupMember.objects.filter(group_id=group_id, user=r.user).delete()
    return redirect("chat:groups")


@login_required
def notifications_view(r: HttpRequest) -> HttpResponse:
    return render(
        r,
        "chat/notifications.html",
        {
            "notifications": Notification.objects.filter(user=r.user)[:50],
            "unread_count": Notification.objects.filter(user=r.user, is_read=False).count(),
        },
    )


@login_required
def notification_read_view(r: HttpRequest, notification_id: int) -> HttpResponse:
    n = get_object_or_404(Notification, pk=notification_id, user=r.user)
    n.is_read = True
    n.save(update_fields=["is_read"])
    return redirect("chat:notifications")


@login_required
def notifications_read_all_view(r: HttpRequest) -> HttpResponse:
    Notification.objects.filter(user=r.user, is_read=False).update(is_read=True)
    return redirect("chat:notifications")
