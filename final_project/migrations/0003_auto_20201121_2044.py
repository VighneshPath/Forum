# Generated by Django 3.0.6 on 2020-11-21 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0002_auto_20201118_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='final_project.Post'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='content',
            field=models.TextField(),
        ),
    ]
