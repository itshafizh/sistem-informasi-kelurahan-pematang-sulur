from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from apps.accounts.mixins import RoleRequiredMixin
from .models import SuratMasuk
from .forms import SuratMasukForm


class SuratMasukListView(RoleRequiredMixin, ListView):
    model = SuratMasuk
    template_name = 'surat_masuk/list.html'
    context_object_name = 'surat_list'
    paginate_by = 15
    allowed_roles = ['admin_kelurahan']

    def get_queryset(self):
        qs = SuratMasuk.objects.all()

        q = self.request.GET.get('q', '').strip()
        tanggal_mulai = self.request.GET.get('tanggal_mulai', '').strip()
        tanggal_akhir = self.request.GET.get('tanggal_akhir', '').strip()
        tahun = self.request.GET.get('tahun', '').strip()
        pengirim = self.request.GET.get('pengirim', '').strip()

        if q:
            qs = qs.filter(
                Q(nomor_surat__icontains=q) |
                Q(asal_pengirim__icontains=q) |
                Q(perihal__icontains=q)
            )

        if tanggal_mulai:
            qs = qs.filter(tanggal_diterima__gte=tanggal_mulai)

        if tanggal_akhir:
            qs = qs.filter(tanggal_diterima__lte=tanggal_akhir)

        if tahun:
            qs = qs.filter(tanggal_diterima__year=tahun)

        if pengirim:
            qs = qs.filter(asal_pengirim__icontains=pengirim)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_values'] = self.request.GET
        return context


class SuratMasukDetailView(RoleRequiredMixin, DetailView):
    model = SuratMasuk
    template_name = 'surat_masuk/detail.html'
    context_object_name = 'surat'
    allowed_roles = ['admin_kelurahan']


class SuratMasukCreateView(RoleRequiredMixin, CreateView):
    model = SuratMasuk
    form_class = SuratMasukForm
    template_name = 'surat_masuk/form.html'
    success_url = reverse_lazy('surat_masuk:list')
    allowed_roles = ['admin_kelurahan']

    def form_valid(self, form):
        form.instance.user_input = self.request.user
        messages.success(self.request, 'Surat masuk berhasil ditambahkan.')
        return super().form_valid(form)


class SuratMasukUpdateView(RoleRequiredMixin, UpdateView):
    model = SuratMasuk
    form_class = SuratMasukForm
    template_name = 'surat_masuk/form.html'
    success_url = reverse_lazy('surat_masuk:list')
    allowed_roles = ['admin_kelurahan']

    def form_valid(self, form):
        messages.success(self.request, 'Surat masuk berhasil diperbarui.')
        return super().form_valid(form)


class SuratMasukDeleteView(RoleRequiredMixin, LoginRequiredMixin, DeleteView):
    model = SuratMasuk
    template_name = 'surat_masuk/confirm_delete.html'
    success_url = reverse_lazy('surat_masuk:list')
    allowed_roles = ['admin_kelurahan']

    def form_valid(self, form):
        messages.success(self.request, 'Surat masuk berhasil dihapus.')
        return super().form_valid(form)