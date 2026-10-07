from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import LoginForm


class SIAKLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Selamat datang, {form.get_user().first_name or form.get_user().username}.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Username atau password salah.")
        return super().form_invalid(form)

    def get_success_url(self):
        # Nanti setelah dashboard dibuat (Tahap 8), redirect ini otomatis
        # mengarah ke 'dashboard:index' sesuai LOGIN_REDIRECT_URL di settings.
        return super().get_success_url()


def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah logout.")
    return redirect('accounts:login')