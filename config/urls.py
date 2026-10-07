from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('surat-masuk/', include('apps.surat_masuk.urls')),
    path('surat-keluar/', include('apps.surat_keluar.urls')),
    path('laporan-pkk/', include('apps.laporan_pkk.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)