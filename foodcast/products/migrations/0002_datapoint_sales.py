# Generated by Django 4.2.5 on 2023-10-01 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('sales_type', models.PositiveSmallIntegerField(verbose_name='Тип')),
                ('sales_units', models.PositiveSmallIntegerField(verbose_name='Продажи, ед.изм')),
                ('sales_units_promo', models.PositiveIntegerField(verbose_name='Продажи в акцию, ед.изм')),
                ('sales_rub', models.PositiveIntegerField(verbose_name='Продажи, руб.')),
                ('sales_rub_promo', models.PositiveIntegerField(verbose_name='Продажи в акцию, руб.')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SKU', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='products.product', verbose_name='SKU')),
                ('fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='products.datapoint', verbose_name='Продажи факт')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='products.shops', verbose_name='ТЦ')),
            ],
        ),
    ]
