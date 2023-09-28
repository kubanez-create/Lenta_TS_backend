from django.db import models


class Product(models.Model):
    """Модель продукта (SKU)"""
    sku = models.CharField(
        max_length=100,
        verbose_name='SKU продукта'
    )
    uom = models.CharField(
        max_length=20,
        verbose_name='UOM еденица измерения'
    )
    group = models.PositiveIntegerField(
        verbose_name='Группа товаров'
    )
    category = models.PositiveIntegerField(
        verbose_name='Категория товаров'
    )
    subcategory = models.PositiveIntegerField(
        verbose_name='Подкатегория товаров'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['sku']
        constraints = [
            models.UniqueConstraint(
                fields=['sku'],
                name='unique sku'
            )
        ]

    def __str__(self):
        return f'SKU - {self.sku}, ед. изм - {self.uom}'


class Shops(models.Model):
    """Модель магазинов"""
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    city = models.CharField(
        max_length=60,
        verbose_name='Город'
    )
    division = models.CharField(
        max_length=60,
        verbose_name='Дивизион'
    )
    type_format = models.PositiveIntegerField(
        verbose_name='Тип Формата'
    )
    loc = models.PositiveIntegerField(
        verbose_name='Локация'
    )
    size = models.PositiveIntegerField(
        verbose_name='Размер'
    )
    is_active = models.BooleanField()

    class Meta:
        verbose_name = 'Магазин ТК'
        verbose_name_plural = 'Магазины ТК'
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique title of shop'
            )
        ]

    def __str__(self):
        return f'Магазин {self.title}, ' \
               f'г. {self.city}, статус - {self.is_active}'
