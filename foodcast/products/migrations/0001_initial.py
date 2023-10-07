# Generated by Django 4.2.5 on 2023-10-07 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Forecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_date', models.DateField(verbose_name='Дата прогноза')),
            ],
            options={
                'verbose_name': 'Прогноз продаж',
                'verbose_name_plural': 'Прогнозы продаж',
                'ordering': ['store'],
            },
        ),
        migrations.CreateModel(
            name='ForecastPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('value', models.PositiveIntegerField(verbose_name='Значение')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sku', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='SKU продукта')),
                ('uom', models.PositiveIntegerField(verbose_name='UOM еденица измерения')),
                ('group', models.CharField(max_length=40, verbose_name='Группа товаров')),
                ('category', models.CharField(max_length=40, verbose_name='Категория товаров')),
                ('subcategory', models.CharField(max_length=40, verbose_name='Подкатегория товаров')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['sku'],
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Shops',
            fields=[
                ('title', models.CharField(max_length=60, primary_key=True, serialize=False, verbose_name='Название')),
                ('city', models.CharField(default='Город', max_length=60, verbose_name='Город')),
                ('division', models.CharField(default='0', max_length=60, verbose_name='Дивизион')),
                ('type_format', models.PositiveIntegerField(default='0', verbose_name='Тип Формата')),
                ('loc', models.PositiveIntegerField(default='0', verbose_name='Локация')),
                ('size', models.PositiveIntegerField(default='0', verbose_name='Размер')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Магазин ТК',
                'verbose_name_plural': 'Магазины ТК',
                'ordering': ['title'],
            },
        ),
        migrations.AddConstraint(
            model_name='shops',
            constraint=models.UniqueConstraint(fields=('title',), name='unique title of shop'),
        ),
        migrations.AddField(
            model_name='sales',
            name='SKU',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='products.product', verbose_name='SKU'),
        ),
        migrations.AddField(
            model_name='sales',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='products.shops', verbose_name='ТЦ'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('sku',), name='unique sku'),
        ),
        migrations.AddField(
            model_name='forecastpoint',
            name='forecast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecast_point', to='products.forecast', verbose_name='Прогноз'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecast', to='products.product', verbose_name='SKU'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecast', to='products.shops', verbose_name='ТЦ'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datapoint', to='products.sales', verbose_name='Реализация'),
        ),
    ]
