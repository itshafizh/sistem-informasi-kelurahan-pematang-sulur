from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from apps.accounts.mixins import RoleRequiredMixin
from .models import SuratKeluar
from .forms import SuratKeluarForm


class SuratKeluarListView(RoleRequiredMixin, ListView):
    model = SuratKeluar
    template_name = 'surat_keluar/list.html'
    context_object_name = 'surat_list'
    paginate_by = 15
    allowed_roles = ['admin_kelurahan']

    def get_queryset(self):
        # Urutan: yang paling baru diinput berada di atas.
        # '-id' sebagai penentu cadangan agar urutan selalu konsisten.
        qs = SuratKeluar.objects.all().order_by('-created_at', '-id')

        q = self.request.GET.get('q', '').strip()
        tanggal_mulai = self.request.GET.get('tanggal_mulai', '').strip()
        tanggal_akhir = self.request.GET.get('tanggal_akhir', '').strip()
        tahun = self.request.GET.get('tahun', '').strip()
        tujuan = self.request.GET.get('tujuan', '').strip()

        if q:
            qs = qs.filter(
                Q(nomor_surat__icontains=q) |
                Q(tujuan_surat__icontains=q) |
                Q(perihal__icontains=q)
            )

        if tanggal_mulai:
            qs = qs.filter(tanggal_surat__gte=tanggal_mulai)

        if tanggal_akhir:
            qs = qs.filter(tanggal_surat__lte=tanggal_akhir)

        if tahun:
            qs = qs.filter(tanggal_surat__year=tahun)

        if tujuan:
            qs = qs.filter(tujuan_surat__icontains=tujuan)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_values'] = self.request.GET
        return context


class SuratKeluarDetailView(RoleRequiredMixin, DetailView):
    model = SuratKeluar
    template_name = 'surat_keluar/detail.html'
    context_object_name = 'surat'
    allowed_roles = ['admin_kelurahan']


class SuratKeluarCreateView(RoleRequiredMixin, CreateView):
    model = SuratKeluar
    form_class = SuratKeluarForm
    template_name = 'surat_keluar/form.html'
    success_url = reverse_lazy('surat_keluar:list')
    allowed_roles = ['admin_kelurahan']

    def form_valid(self, form):
        form.instance.user_input = self.request.user
        messages.success(self.request, 'Surat keluar berhasil ditambahkan.')
        return super().form_valid(form)


class SuratKeluarUpdateView(RoleRequiredMixin, UpdateView):
    model = SuratKeluar
    form_class = SuratKeluarForm
    template_name = 'surat_keluar/form.html'
    success_url = reverse_lazy('surat_keluar:list')
    allowed_roles = ['admin_kelurahan']

    def form_valid(self, form):
        messages.success(self.request, 'Surat keluar berhasil diperbarui.')
        return super().form_valid(form)


class SuratKeluarDeleteView(RoleRequiredMixin, DeleteView):
    model = SuratKeluar
    template_name = 'surat_keluar/confirm_delete.html'
    success_url = reverse_lazy('surat_keluar:list')
    allowed_roles = ['admin_kelurahan']

    def form_valid(self, form):
        messages.success(self.request, 'Surat keluar berhasil dihapus.')
        return super().form_valid(form)