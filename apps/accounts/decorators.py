from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    """
    Decorator untuk Function-Based View.
    Contoh pemakaian:

        @role_required('admin_kelurahan')
        def tambah_surat_masuk(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            profile = getattr(request.user, 'profile', None)
            if profile is None or profile.role.nama_role not in allowed_roles:
                raise PermissionDenied("Anda tidak memiliki akses ke halaman ini.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator