from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View

from apps.accounts.mixins import RoleRequiredMixin
from .models import LaporanPKK
from .forms import LaporanPKKForm, DokumentasiFormSet, StatusUpdateForm


class LaporanPKKListView(RoleRequiredMixin, ListView):
    model = LaporanPKK
    template_name = 'laporan_pkk/list.html'
    context_object_name = 'laporan_list'
    paginate_by = 15
    # Baik admin maupun pengurus PKK boleh melihat daftar laporan (poin 3),
    # bedanya nanti hanya admin yang bisa ubah status/hapus (dibatasi di view lain).
    allowed_roles = ['admin_kelurahan', 'pengurus_pkk']

    def get_queryset(self):
        qs = LaporanPKK.objects.select_related('pokja').all()

        bulan = self.request.GET.get('bulan', '').strip()
        tahun = self.request.GET.get('tahun', '').strip()
        pokja_id = self.request.GET.get('pokja', '').strip()
        rt_rw = self.request.GET.get('rt_rw', '').strip()
        status = self.request.GET.get('status', '').strip()

        if bulan:
            qs = qs.filter(tanggal_kegiatan__month=bulan)
        if tahun:
            qs = qs.filter(tanggal_kegiatan__year=tahun)
        if pokja_id:
            qs = qs.filter(pokja_id=pokja_id)
        if rt_rw:
            qs = qs.filter(rt_rw__icontains=rt_rw)
        if status:
            qs = qs.filter(status=status)

        return qs

    def get_context_data(self, **kwargs):
        from apps.master_data.models import Pokja
        context = super().get_context_data(**kwargs)

        context['pokja_options'] = Pokja.objects.all()
        context['status_options'] = LaporanPKK.STATUS_CHOICES
        context['filter_values'] = self.request.GET

        # Statistik total & per pokja (mengikuti filter yang aktif, kecuali filter pokja itu sendiri)
        base_qs = self.get_queryset()
        context['total_kegiatan'] = base_qs.count()
        context['statistik_pokja'] = (
            base_qs.values('pokja__nama_pokja')
            .annotate(total=Count('id'))
            .order_by('pokja__nama_pokja')
        )
        return context


class LaporanPKKDetailView(RoleRequiredMixin, DetailView):
    model = LaporanPKK
    template_name = 'laporan_pkk/detail.html'
    context_object_name = 'laporan'
    allowed_roles = ['admin_kelurahan', 'pengurus_pkk']


class LaporanPKKCreateView(RoleRequiredMixin, CreateView):
    model = LaporanPKK
    form_class = LaporanPKKForm
    template_name = 'laporan_pkk/form.html'
    success_url = reverse_lazy('laporan_pkk:list')
    # Hanya admin yang bisa input manual (poin 3: pengurus PKK tidak mengelola administrasi)
    allowed_roles = ['admin_kelurahan']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DokumentasiFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = DokumentasiFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Laporan PKK berhasil ditambahkan.')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LaporanPKKUpdateView(RoleRequiredMixin, UpdateView):
    model = LaporanPKK
    form_class = LaporanPKKForm
    template_name = 'laporan_pkk/form.html'
    success_url = reverse_lazy('laporan_pkk:list')
    allowed_roles = ['admin_kelurahan']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DokumentasiFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = DokumentasiFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Laporan PKK berhasil diperbarui.')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LaporanPKKDeleteView(RoleRequiredMixin, DeleteView):
    model = LaporanPKK
    template_name = 'laporan_pkk/confirm_delete.html'
    success_url = reverse_lazy('laporan_pkk:list')
    allowed_roles = ['admin_kelurahan']

    def form_valid(self, form):
        messages.success(self.request, 'Laporan PKK berhasil dihapus.')
        return super().form_valid(form)


class LaporanPKKStatusUpdateView(RoleRequiredMixin, UpdateView):
    """View terpisah khusus untuk verifikasi status + catatan (poin 8)."""
    model = LaporanPKK
    form_class = StatusUpdateForm
    template_name = 'laporan_pkk/status_form.html'
    allowed_roles = ['admin_kelurahan']

    def get_success_url(self):
        messages.success(self.request, 'Status laporan berhasil diperbarui.')
        return reverse_lazy('laporan_pkk:detail', kwargs={'pk': self.object.pk})