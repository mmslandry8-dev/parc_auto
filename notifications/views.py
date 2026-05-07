from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Notification

@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'notifications/list.html',
        {
            'notifications': notifications
        }
    )

@login_required
def mark_as_read(request, pk):

    notif = get_object_or_404(
        Notification,
        id=pk,
        user=request.user
    )

    notif.is_read = True

    notif.save()

    return redirect('notification_list')