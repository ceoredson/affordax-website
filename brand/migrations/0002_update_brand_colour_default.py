from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("brand", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteidentity",
            name="primary_colour",
            field=models.CharField(default="#ce1126", max_length=7),
        ),
    ]
