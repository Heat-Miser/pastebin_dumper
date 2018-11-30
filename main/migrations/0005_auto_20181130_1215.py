# Generated by Django 2.1.3 on 2018-11-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_pastie_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regex', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='pastie',
            options={},
        ),
        migrations.AddField(
            model_name='pastie',
            name='keep',
            field=models.BooleanField(default=False),
        ),
    ]
