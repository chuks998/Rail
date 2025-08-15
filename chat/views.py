from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def chat_messages_json(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user))
        | (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by("timestamp")
    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "sender_id": msg.sender.id,
            "message": msg.message,
            "image_url": msg.image.url if msg.image else "",
            "timestamp": msg.timestamp.strftime("%H:%M, %b %d"),
        }
        for msg in messages
    ]
    return JsonResponse({"messages": data})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ChatMessage
from django.http import JsonResponse
from django.db.models import Q

User = get_user_model()


@login_required
def chat_list(request):
    if request.user.is_superuser:
        # Admin: show only users who have sent messages to admin
        user_ids = (
            ChatMessage.objects.filter(receiver=request.user)
            .values_list("sender", flat=True)
            .distinct()
        )
        users = User.objects.filter(id__in=user_ids)
    else:
        # Normal user: show only admin(s)
        users = User.objects.filter(is_superuser=True).exclude(id=request.user.id)
    return render(request, "chat/chat_list.html", {"users": users})


@login_required
def chat_room(request, user_id):
    # Show chat between current user and selected user (or admin)
    other_user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        message = request.POST.get("message", "")
        image = request.FILES.get("image")
        if message or image:
            ChatMessage.objects.create(
                sender=request.user, receiver=other_user, message=message, image=image
            )
        return redirect("chat_room", user_id=other_user.id)
    # Mark all unread messages from other_user to current user as read
    ChatMessage.objects.filter(
        sender=other_user, receiver=request.user, is_read=False
    ).update(is_read=True)
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user))
        | (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by("timestamp")
    return render(
        request, "chat/chat_room.html", {"other_user": other_user, "messages": messages}
    )


@login_required
def send_message(request, user_id):
    if request.method == "POST":
        other_user = get_object_or_404(User, id=user_id)
        message = request.POST.get("message", "")
        image = request.FILES.get("image")
        chat_message = ChatMessage.objects.create(
            sender=request.user, receiver=other_user, message=message, image=image
        )
        if request.is_ajax():
            return JsonResponse({"status": "ok"})
        return redirect("chat_room", user_id=other_user.id)
    return JsonResponse({"status": "error"}, status=400)
