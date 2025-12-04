from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @login_required(login_url="/login/")
        def wrapper(request, *args, **kwargs):

            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # ROLE NOT ALLOWED
            return redirect('/login')

        return wrapper
    return decorator