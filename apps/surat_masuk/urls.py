from django.urls import path
from . import views

app_name = 'surat_masuk'

urlpatterns = [
    path('', views.SuratMasukListView.as_view(), name='list'),
    path('tambah/', views.SuratMasukCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SuratMasukDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.SuratMasukUpdateView.as_view(), name='update'),
    path('<int:pk>/hapus/', views.SuratMasukDeleteView.as_view(), name='delete'),
]