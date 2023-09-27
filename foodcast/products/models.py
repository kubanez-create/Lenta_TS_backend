from django.db import models


class ProductGroup(models.Model):
    """Модель групп товаров"""
    title = models.CharField(
        max_length=100,
        verbose_name='Группа товаров'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique sku group'
            )
        ]

    def __str__(self):
        return f'Группа товаров - {self.title}'


class ProductCategory(models.Model):
    """Модель категорий товаров группы"""
    title = models.CharField(
        max_length=100,
        verbose_name='Категория товаров'
    )
    group = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='category_group',
        verbose_name='Категория группы товаров'
    )

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique sku category'
            )
        ]

    def __str__(self):
        return f'Категория - {self.title}'


class ProductSubCategory(models.Model):
    """Модель подкатегории товара"""
    title = models.CharField(
        max_length=100,
        verbose_name='Подкатегория товаров'
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='sub_category',
        verbose_name='Подкатегория товаров'
    )

    class Meta:
        verbose_name = 'Подкатегория товара'
        verbose_name_plural = 'Подкатегории товаров'
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique sku sub_category'
            )
        ]

    def __str__(self):
        return f'Подкатегория - {self.title}'


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
    group = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='product_group',
        verbose_name='Группа'
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='product_category',
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        ProductSubCategory,
        on_delete=models.CASCADE,
        related_name='product_subcategory',
        verbose_name='Подкатегория'
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
