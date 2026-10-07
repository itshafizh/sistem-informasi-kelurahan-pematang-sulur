from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import LaporanPKK, DokumentasiPKK

ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']
MAX_FILE_SIZE_MB = 5


class LaporanPKKForm(forms.ModelForm):
    class Meta:
        model = LaporanPKK
        fields = [
            'nama_pelapor', 'pokja', 'rt_rw', 'nama_kegiatan', 'tanggal_kegiatan',
            'lokasi_kegiatan', 'jumlah_peserta', 'uraian_kegiatan', 'hasil_kegiatan',
            'kendala',
        ]
        widgets = {
            'nama_pelapor': forms.TextInput(attrs={'class': 'form-control'}),
            'pokja': forms.Select(attrs={'class': 'form-select'}),
            'rt_rw': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RT 01/RW 02'}),
            'nama_kegiatan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_kegiatan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lokasi_kegiatan': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah_peserta': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'uraian_kegiatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hasil_kegiatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'kendala': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.sumber_data = LaporanPKK.SUMBER_MANUAL
        if commit:
            instance.save()
        return instance


class DokumentasiPKKForm(forms.ModelForm):
    class Meta:
        model = DokumentasiPKK
        fields = ['file_dokumentasi', 'keterangan']
        widgets = {
            'file_dokumentasi': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'keterangan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keterangan foto (opsional)'}),
        }

    def clean_file_dokumentasi(self):
        file = self.cleaned_data.get('file_dokumentasi')
        if not file:
            return file

        ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError(
                f"Tipe file tidak diizinkan. Gunakan: {', '.join(ALLOWED_EXTENSIONS).upper()}."
            )

        max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
        if file.size > max_size_bytes:
            raise ValidationError(f"Ukuran file maksimal {MAX_FILE_SIZE_MB} MB.")

        return file


DokumentasiFormSet = inlineformset_factory(
    LaporanPKK,
    DokumentasiPKK,
    form=DokumentasiPKKForm,
    fields=['file_dokumentasi', 'keterangan'],
    extra=2,
    can_delete=True,
)


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = LaporanPKK
        fields = ['status', 'catatan_admin']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'catatan_admin': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Wajib diisi jika status "Perlu Revisi"'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        catatan = cleaned_data.get('catatan_admin', '').strip()

        if status == LaporanPKK.STATUS_REVISI and not catatan:
            raise ValidationError({
                'catatan_admin': 'Catatan wajib diisi jika status "Perlu Revisi".'
            })

        return cleaned_data