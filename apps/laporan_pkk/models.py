from django.db import models
from apps.master_data.models import Pokja


class LaporanPKK(models.Model):
    STATUS_MENUNGGU = 'menunggu_verifikasi'
    STATUS_DISETUJUI = 'disetujui'
    STATUS_REVISI = 'perlu_revisi'
    STATUS_CHOICES = [
        (STATUS_MENUNGGU, 'Menunggu Verifikasi'),
        (STATUS_DISETUJUI, 'Disetujui'),
        (STATUS_REVISI, 'Perlu Revisi'),
    ]

    SUMBER_MANUAL = 'manual'
    SUMBER_GOOGLE_SHEET = 'google_sheet'
    SUMBER_CHOICES = [
        (SUMBER_MANUAL, 'Input Manual'),
        (SUMBER_GOOGLE_SHEET, 'Google Sheet'),
    ]

    nama_pelapor = models.CharField(max_length=150)
    pokja = models.ForeignKey(Pokja, on_delete=models.PROTECT, related_name='laporan_set')
    rt_rw = models.CharField(max_length=20)
    nama_kegiatan = models.CharField(max_length=255)
    tanggal_kegiatan = models.DateField()
    lokasi_kegiatan = models.CharField(max_length=255)
    jumlah_peserta = models.PositiveIntegerField(default=0)
    uraian_kegiatan = models.TextField()
    hasil_kegiatan = models.TextField(blank=True)
    kendala = models.TextField(blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=STATUS_MENUNGGU)
    catatan_admin = models.TextField(blank=True)
    sumber_data = models.CharField(max_length=15, choices=SUMBER_CHOICES, default=SUMBER_MANUAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'laporan_pkk'
        verbose_name = 'Laporan Kegiatan PKK'
        verbose_name_plural = 'Laporan Kegiatan PKK'
        ordering = ['-tanggal_kegiatan']

    def __str__(self):
        return f"{self.nama_kegiatan} - {self.pokja.nama_pokja}"


class DokumentasiPKK(models.Model):
    laporan = models.ForeignKey(LaporanPKK, on_delete=models.CASCADE, related_name='dokumentasi_set')
    file_dokumentasi = models.FileField(upload_to='dokumentasi_pkk/%Y/')
    keterangan = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dokumentasi_pkk'
        verbose_name = 'Dokumentasi Kegiatan PKK'
        verbose_name_plural = 'Dokumentasi Kegiatan PKK'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Dokumentasi - {self.laporan.nama_kegiatan}"