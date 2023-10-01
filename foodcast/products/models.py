from django.db import models


class Product(models.Model):
    """Модель продукта (SKU)."""
    sku = models.CharField(
        max_length=40,
        verbose_name='SKU продукта',
        primary_key=True,
    )
    uom = models.PositiveIntegerField(
        verbose_name='UOM еденица измерения'
    )
    group = models.CharField(
        max_length=40,
        verbose_name='Группа товаров'
    )
    category =models.CharField(
        max_length=40,
        verbose_name='Категория товаров'
    )
    subcategory = models.CharField(
        max_length=40,
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
    """Модель магазинов."""
    title = models.CharField(
        max_length=60,
        verbose_name='Название',
        primary_key=True,
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


class DataPoint(models.Model):
    date = models.DateField(verbose_name="Дата")
    sales_type = models.PositiveSmallIntegerField(verbose_name="Тип")
    sales_units = models.PositiveSmallIntegerField(
        verbose_name="Продажи, ед.изм")
    sales_units_promo = models.PositiveIntegerField(
        verbose_name="Продажи в акцию, ед.изм")
    sales_rub = models.PositiveIntegerField(
        verbose_name="Продажи, руб.")
    sales_rub_promo = models.PositiveIntegerField(
        verbose_name="Продажи в акцию, руб.")
    sale = models.ForeignKey(
        "Sales",
        verbose_name="Реализация",
        related_name="datapoint",
        on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']


class Sales(models.Model):
    store = models.ForeignKey(
        Shops,
        verbose_name="ТЦ",
        related_name="sales",
        on_delete=models.CASCADE
    )
    SKU = models.ForeignKey(
        Product,
        verbose_name="SKU",
        related_name="sales",
        on_delete=models.CASCADE
    )
