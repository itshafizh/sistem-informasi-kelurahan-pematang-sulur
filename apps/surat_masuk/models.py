from django.db import models
from django.conf import settings


class SuratMasuk(models.Model):
    nomor_surat = models.CharField(max_length=100, verbose_name='No. Surat yang Diterima')
    tanggal_surat = models.DateField()
    tanggal_diterima = models.DateField(verbose_name='Tanggal Terima Surat')
    asal_pengirim = models.CharField(max_length=150, verbose_name='Dari')
    perihal = models.CharField(max_length=255)
    lampiran = models.CharField(max_length=100, blank=True, help_text='Contoh: 1 lembar')
    ditujukan_kepada = models.CharField(max_length=150, blank=True, verbose_name='Diteruskan Kepada')
    file_surat = models.FileField(upload_to='surat_masuk/%Y/')
    user_input = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='surat_masuk_diinput'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'surat_masuk'
        verbose_name = 'Surat Masuk'
        verbose_name_plural = 'Surat Masuk'
        ordering = ['-tanggal_diterima']

    def __str__(self):
        return f"{self.nomor_surat} - {self.perihal}"