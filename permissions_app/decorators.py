from functools import wraps

from django.shortcuts import redirect


def role_required(*roles):
    """Restrict a view to authenticated users with one of the supplied roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect("login")

            # Repair older accounts that were created before profile signals existed.
            from accounts.models import UserProfile
            if user.is_superuser:
                fallback_role = "admin"
            elif user.is_staff:
                fallback_role = "teacher"
            else:
                fallback_role = "student"
            profile, _ = UserProfile.objects.get_or_create(
                user=user, defaults={"role": fallback_role}
            )

            if profile.role not in roles:
                return redirect("main_dashboard")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
