from django.urls import path
from . import views

app_name = 'surat_keluar'

urlpatterns = [
    path('', views.SuratKeluarListView.as_view(), name='list'),
    path('tambah/', views.SuratKeluarCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SuratKeluarDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.SuratKeluarUpdateView.as_view(), name='update'),
    path('<int:pk>/hapus/', views.SuratKeluarDeleteView.as_view(), name='delete'),
]