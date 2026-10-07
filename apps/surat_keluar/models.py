from django.db import models
from django.conf import settings


class SuratKeluar(models.Model):
    nomor_surat = models.CharField(max_length=100)
    tanggal_surat = models.DateField()
    tujuan_surat = models.CharField(max_length=150, verbose_name='Kepada')
    perihal = models.CharField(max_length=255)
    lampiran = models.CharField(max_length=100, blank=True, help_text='Contoh: 1 lembar')
    tembusan = models.CharField(max_length=255, blank=True)
    file_surat = models.FileField(upload_to='surat_keluar/%Y/')
    user_input = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='surat_keluar_diinput'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'surat_keluar'
        verbose_name = 'Surat Keluar'
        verbose_name_plural = 'Surat Keluar'
        ordering = ['-tanggal_surat']

    def __str__(self):
        return f"{self.nomor_surat} - {self.perihal}"