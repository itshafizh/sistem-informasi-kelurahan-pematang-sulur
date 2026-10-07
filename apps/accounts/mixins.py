from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin untuk Class-Based View (dipakai nanti di ListView/CreateView modul
    Surat Masuk, Surat Keluar, Laporan PKK).

    Contoh pemakaian:

        class SuratMasukListView(RoleRequiredMixin, ListView):
            allowed_roles = ['admin_kelurahan']
            ...
    """
    allowed_roles = []

    def test_func(self):
        profile = getattr(self.request.user, 'profile', None)
        if profile is None:
            return False
        return profile.role.nama_role in self.allowed_roles

    def handle_no_permission(self):
        from django.core.exceptions import PermissionDenied
        if self.request.user.is_authenticated:
            raise PermissionDenied("Anda tidak memiliki akses ke halaman ini.")
        return super().handle_no_permission()