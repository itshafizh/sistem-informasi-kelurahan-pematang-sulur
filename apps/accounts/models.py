from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    """
    Tabel referensi role. Minimal berisi 2 baris data (diisi lewat migration
    data atau admin panel nanti): 'admin_kelurahan' dan 'pengurus_pkk'.
    """
    nama_role = models.CharField(max_length=50, unique=True)
    deskripsi = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nama_role


class Profile(models.Model):
    """
    Extend User bawaan Django (bukan bikin tabel users dari nol) agar
    password tetap di-hash otomatis oleh sistem auth Django (poin 15).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='profiles')
    nama_lengkap = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile Pengguna'
        verbose_name_plural = 'Profile Pengguna'

    def __str__(self):
        return f"{self.nama_lengkap} ({self.role.nama_role})"