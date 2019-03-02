# Generated by Django 2.1.7 on 2019-03-02 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190301_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='approved_commment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='post1',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Post'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author1',
            field=models.CharField(max_length=200),
        ),
    ]
