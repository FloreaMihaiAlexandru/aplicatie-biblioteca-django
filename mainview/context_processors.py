from django.contrib.auth import get_user_model


def user_context_processor(request):
    if request.user.is_authenticated and request.user.is_staff:
        User = get_user_model()
        pending_users = User.objects.all().filter(is_active=False).count()
        return {'pending_users': pending_users}
    return {}