from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "authentication/login.html")

@login_required
def dashboard(request):
    user = request.user

    unread_notification = Notification.objects.filter(user=user, is_read=False)
    unread_notification_count = unread_notification.count()
    context = {
        'unread_notification': unread_notification,
        'unread_notification_count': unread_notification_count,
    }

    if user.is_admin:
        # return render(request, "admin/admin-dashboard.html", context)
        return render(request, "students/student-dashboard.html", context)
    elif user.is_teacher:
        # return render(request, "teachers/teacher-dashboard.html", context)
        return render(request, "students/student-dashboard.html", context)
    elif user.is_student:
        return render(request, "students/student-dashboard.html", context)
    else:
        return redirect("index")


def mark_notification_as_read(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

def clear_all_notifications(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden