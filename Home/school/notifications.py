from .models import Notification

# Funzione per creare una notifica
def create_notification(user, message):
    Notification.objects.create(user=user, message=message)

# Context processor per rendere disponibili le notifiche globali
def notification_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {
            'unread_notification': notifications,
            'unread_notification_count': notifications.count()
        }
    return {}