from django import forms
from django.core.exceptions import ValidationError
from .models import SuratKeluar

ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']
MAX_FILE_SIZE_MB = 5


class SuratKeluarForm(forms.ModelForm):
    class Meta:
        model = SuratKeluar
        fields = [
            'nomor_surat', 'tanggal_surat', 'tujuan_surat', 'perihal',
            'lampiran', 'tembusan', 'file_surat',
        ]
        labels = {
            'nomor_surat': 'Nomor Surat',
            'tanggal_surat': 'Tanggal Surat',
            'tujuan_surat': 'Kepada',
            'perihal': 'Perihal',
            'lampiran': 'Lampiran',
            'tembusan': 'Tembusan',
            'file_surat': 'Upload File',
        }
        widgets = {
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_surat': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tujuan_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'perihal': forms.TextInput(attrs={'class': 'form-control'}),
            'lampiran': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 1 lembar'}),
            'tembusan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Camat, Sekretaris Kelurahan'}),
            'file_surat': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file_surat(self):
        file = self.cleaned_data.get('file_surat')
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