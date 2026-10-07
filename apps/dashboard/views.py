from datetime import date
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.views.generic import TemplateView

from apps.accounts.mixins import RoleRequiredMixin
from apps.surat_masuk.models import SuratMasuk
from apps.surat_keluar.models import SuratKeluar
from apps.laporan_pkk.models import LaporanPKK


class DashboardView(RoleRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    allowed_roles = ['admin_kelurahan', 'pengurus_pkk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        # --- Statistik dasar (poin 4) ---
        context['total_surat_masuk'] = SuratMasuk.objects.count()
        context['total_surat_keluar'] = SuratKeluar.objects.count()
        context['total_laporan_pkk'] = LaporanPKK.objects.count()

        context['surat_masuk_bulan_ini'] = SuratMasuk.objects.filter(
            tanggal_diterima__year=today.year, tanggal_diterima__month=today.month
        ).count()
        context['surat_keluar_bulan_ini'] = SuratKeluar.objects.filter(
            tanggal_surat__year=today.year, tanggal_surat__month=today.month
        ).count()
        context['laporan_pkk_bulan_ini'] = LaporanPKK.objects.filter(
            tanggal_kegiatan__year=today.year, tanggal_kegiatan__month=today.month
        ).count()

        # --- Statistik surat per bulan (tabel, bukan chart) ---
        surat_masuk_per_bulan = (
            SuratMasuk.objects
            .annotate(bulan=TruncMonth('tanggal_diterima'))
            .values('bulan')
            .annotate(total=Count('id'))
            .order_by('-bulan')
        )
        surat_keluar_per_bulan = (
            SuratKeluar.objects
            .annotate(bulan=TruncMonth('tanggal_surat'))
            .values('bulan')
            .annotate(total=Count('id'))
            .order_by('-bulan')
        )

        # Gabungkan surat masuk & keluar jadi satu tabel per bulan
        gabungan = {}
        for item in surat_masuk_per_bulan:
            key = item['bulan']
            gabungan.setdefault(key, {'bulan': key, 'masuk': 0, 'keluar': 0})
            gabungan[key]['masuk'] = item['total']
        for item in surat_keluar_per_bulan:
            key = item['bulan']
            gabungan.setdefault(key, {'bulan': key, 'masuk': 0, 'keluar': 0})
            gabungan[key]['keluar'] = item['total']

        context['statistik_surat_bulanan'] = sorted(
            gabungan.values(), key=lambda x: x['bulan'], reverse=True
        )

        # --- Statistik kegiatan PKK per Pokja (poin 4) ---
        context['statistik_pokja'] = (
            LaporanPKK.objects
            .values('pokja__nama_pokja')
            .annotate(total=Count('id'))
            .order_by('pokja__nama_pokja')
        )

        return context