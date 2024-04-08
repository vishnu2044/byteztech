# Generated by Django 5.0.4 on 2024-04-07 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_auth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="uploads/")),
                ("file_type", models.CharField(max_length=100)),
                ("file_size", models.IntegerField()),
            ],
        ),
    ]