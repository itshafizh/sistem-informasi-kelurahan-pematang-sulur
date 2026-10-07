from django.db import migrations


def seed_pokja(apps, schema_editor):
    Pokja = apps.get_model('master_data', 'Pokja')
    data = [
        ('Pokja I', 'Penghayatan dan Pengamalan Pancasila serta Gotong Royong'),
        ('Pokja II', 'Pendidikan dan Keterampilan serta Pengembangan Kehidupan Berkoperasi'),
        ('Pokja III', 'Pangan, Sandang, dan Perumahan Tata Laksana Rumah Tangga'),
        ('Pokja IV', 'Kesehatan, Kelestarian Lingkungan Hidup, dan Perencanaan Sehat'),
    ]
    for nama, deskripsi in data:
        Pokja.objects.get_or_create(nama_pokja=nama, defaults={'deskripsi': deskripsi})


def unseed_pokja(apps, schema_editor):
    Pokja = apps.get_model('master_data', 'Pokja')
    Pokja.objects.filter(nama_pokja__in=['Pokja I', 'Pokja II', 'Pokja III', 'Pokja IV']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_pokja, unseed_pokja),
    ]