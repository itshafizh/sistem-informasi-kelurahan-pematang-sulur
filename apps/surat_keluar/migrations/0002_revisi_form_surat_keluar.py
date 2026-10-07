from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surat_keluar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suratkeluar',
            name='jenis_surat',
        ),
        migrations.RemoveField(
            model_name='suratkeluar',
            name='nomor_agenda',
        ),
        migrations.RemoveField(
            model_name='suratkeluar',
            name='penandatangan',
        ),
        migrations.RemoveField(
            model_name='suratkeluar',
            name='keterangan',
        ),
        migrations.AddField(
            model_name='suratkeluar',
            name='lampiran',
            field=models.CharField(blank=True, help_text='Contoh: 1 lembar', max_length=100),
        ),
        migrations.AddField(
            model_name='suratkeluar',
            name='tembusan',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='suratkeluar',
            name='tujuan_surat',
            field=models.CharField(max_length=150, verbose_name='Kepada'),
        ),
    ]