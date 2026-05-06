import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MediaAsset",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="uploads/%Y/%m/%d/")),
                ("content_type", models.CharField(max_length=120)),
                ("size", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="media_assets", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(model_name="mediaasset", index=models.Index(fields=["owner", "-created_at"], name="mediafiles_owner_i_c698f7_idx")),
    ]
