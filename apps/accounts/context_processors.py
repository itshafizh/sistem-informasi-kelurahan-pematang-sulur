def sidebar_info(request):
    """Jumlah laporan PKK yang menunggu verifikasi, untuk lencana di sidebar.
    Hanya dihitung untuk Admin Kelurahan. Peran lain mendapat 0 (lencana tidak tampil)."""
    jumlah = 0

    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        profile = getattr(user, 'profile', None)
        if profile is not None and profile.role.nama_role == 'admin_kelurahan':
            from apps.laporan_pkk.models import LaporanPKK
            jumlah = LaporanPKK.objects.filter(status=LaporanPKK.STATUS_MENUNGGU).count()

    return {'sidebar_menunggu_verifikasi': jumlah}