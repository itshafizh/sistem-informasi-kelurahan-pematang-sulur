from django.urls import path
from . import views

app_name = 'laporan_pkk'

urlpatterns = [
    path('', views.LaporanPKKListView.as_view(), name='list'),
    path('tambah/', views.LaporanPKKCreateView.as_view(), name='create'),
    path('<int:pk>/', views.LaporanPKKDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.LaporanPKKUpdateView.as_view(), name='update'),
    path('<int:pk>/hapus/', views.LaporanPKKDeleteView.as_view(), name='delete'),
    path('<int:pk>/status/', views.LaporanPKKStatusUpdateView.as_view(), name='status_update'),
]