from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surat_masuk', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suratmasuk',
            name='jenis_surat',
        ),
        migrations.RemoveField(
            model_name='suratmasuk',
            name='nomor_agenda',
        ),
        migrations.RemoveField(
            model_name='suratmasuk',
            name='keterangan',
        ),
        migrations.AddField(
            model_name='suratmasuk',
            name='lampiran',
            field=models.CharField(blank=True, help_text='Contoh: 1 lembar', max_length=100),
        ),
    ]