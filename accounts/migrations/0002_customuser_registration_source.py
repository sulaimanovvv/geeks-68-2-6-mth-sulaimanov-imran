from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="registration_source",
            field=models.CharField(
                default="local",
                max_length=20,
                verbose_name="источник регистрации",
            ),
        ),
    ]
