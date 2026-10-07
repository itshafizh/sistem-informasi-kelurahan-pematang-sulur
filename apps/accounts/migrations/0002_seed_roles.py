from django.db import migrations


def seed_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    Role.objects.get_or_create(
        nama_role='admin_kelurahan',
        defaults={'deskripsi': 'Admin Kelurahan - akses penuh administrasi surat'}
    )
    Role.objects.get_or_create(
        nama_role='pengurus_pkk',
        defaults={'deskripsi': 'Pengurus PKK - akses laporan kegiatan PKK'}
    )


def unseed_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    Role.objects.filter(nama_role__in=['admin_kelurahan', 'pengurus_pkk']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_roles, unseed_roles),
    ]