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
            name="Chat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(choices=[("direct", "Direct"), ("group", "Group")], max_length=16)),
                ("title", models.CharField(blank=True, max_length=160)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_chats", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ChatMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("member", "Member"), ("admin", "Admin")], default="member", max_length=16)),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("muted_until", models.DateTimeField(blank=True, null=True)),
                ("chat", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="chats.chat")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="chat_memberships", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name="chat",
            name="participants",
            field=models.ManyToManyField(related_name="chats", through="chats.ChatMember", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("sent", "Sent"), ("delivered", "Delivered"), ("read", "Read")], default="sent", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("edited_at", models.DateTimeField(blank=True, null=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("chat", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="chats.chat")),
                ("reply_to", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="chats.message")),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ReadReceipt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("read_at", models.DateTimeField(auto_now_add=True)),
                ("message", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="read_receipts", to="chats.message")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="read_receipts", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(model_name="chat", index=models.Index(fields=["type", "-updated_at"], name="chats_chat_type_6dfc64_idx")),
        migrations.AddIndex(model_name="chatmember", index=models.Index(fields=["user", "chat"], name="chats_chatm_user_id_464cdb_idx")),
        migrations.AddIndex(model_name="message", index=models.Index(fields=["chat", "-created_at"], name="chats_messa_chat_id_1072ff_idx")),
        migrations.AddIndex(model_name="message", index=models.Index(fields=["sender", "-created_at"], name="chats_messa_sender__f47136_idx")),
        migrations.AddConstraint(model_name="chatmember", constraint=models.UniqueConstraint(fields=("chat", "user"), name="unique_chat_member")),
        migrations.AddConstraint(model_name="readreceipt", constraint=models.UniqueConstraint(fields=("message", "user"), name="unique_message_reader")),
    ]
