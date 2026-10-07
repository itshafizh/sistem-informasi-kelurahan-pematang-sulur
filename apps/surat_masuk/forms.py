from django import forms
from django.core.exceptions import ValidationError
from .models import SuratMasuk

ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']
MAX_FILE_SIZE_MB = 5


class SuratMasukForm(forms.ModelForm):
    class Meta:
        model = SuratMasuk
        fields = [
            'nomor_surat', 'tanggal_surat', 'tanggal_diterima', 'asal_pengirim',
            'perihal', 'lampiran', 'ditujukan_kepada', 'file_surat',
        ]
        labels = {
            'nomor_surat': 'No. Surat yang Diterima',
            'tanggal_surat': 'Tanggal Surat',
            'tanggal_diterima': 'Tanggal Terima Surat',
            'asal_pengirim': 'Dari',
            'perihal': 'Perihal',
            'lampiran': 'Lampiran',
            'ditujukan_kepada': 'Diteruskan Kepada',
            'file_surat': 'Upload File',
        }
        widgets = {
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_surat': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_diterima': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'asal_pengirim': forms.TextInput(attrs={'class': 'form-control'}),
            'perihal': forms.TextInput(attrs={'class': 'form-control'}),
            'lampiran': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 1 lembar'}),
            'ditujukan_kepada': forms.TextInput(attrs={'class': 'form-control'}),
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

    def clean(self):
        cleaned_data = super().clean()
        tanggal_surat = cleaned_data.get('tanggal_surat')
        tanggal_diterima = cleaned_data.get('tanggal_diterima')

        if tanggal_surat and tanggal_diterima and tanggal_diterima < tanggal_surat:
            raise ValidationError("Tanggal diterima tidak boleh sebelum tanggal surat.")

        return cleaned_data


class SuratMasukFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Pencarian')
    tanggal_mulai = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    tanggal_akhir = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    tahun = forms.CharField(required=False)
    pengirim = forms.CharField(required=False)