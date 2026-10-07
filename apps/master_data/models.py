from django.db import models


class JenisSurat(models.Model):
    KATEGORI_MASUK = 'masuk'
    KATEGORI_KELUAR = 'keluar'
    KATEGORI_KEDUANYA = 'keduanya'
    KATEGORI_CHOICES = [
        (KATEGORI_MASUK, 'Surat Masuk'),
        (KATEGORI_KELUAR, 'Surat Keluar'),
        (KATEGORI_KEDUANYA, 'Keduanya'),
    ]

    nama_jenis = models.CharField(max_length=100)
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICES, default=KATEGORI_KEDUANYA)

    class Meta:
        db_table = 'jenis_surat'
        verbose_name = 'Jenis Surat'
        verbose_name_plural = 'Jenis Surat'
        ordering = ['nama_jenis']

    def __str__(self):
        return self.nama_jenis


class Pokja(models.Model):
    nama_pokja = models.CharField(max_length=50, unique=True)
    deskripsi = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'pokja'
        verbose_name = 'Pokja PKK'
        verbose_name_plural = 'Pokja PKK'
        ordering = ['nama_pokja']

    def __str__(self):
        return self.nama_pokja