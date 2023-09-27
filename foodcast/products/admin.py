from django.contrib import admin

from .models import (
    ProductGroup,
    ProductCategory,
    ProductSubCategory,
    Product,
    Shops
)
from users.models import CustomUser


class GroupsAbmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'group')
    list_filter = ('group',)
    search_fields = ['title']


class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ['title']


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'group', 'subcategory')
    list_display = ('sku', 'uom', 'group', 'category', 'subcategory')
    search_fields = ['sku']


class ShopsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'city',
        'division',
        'type_format',
        'loc',
        'size',
        'is_active'
    )
    list_filter = ('city', 'is_active')
    search_fields = ['title']


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'password', 'is_superuser')
    list_filter = ('email',)
    search_fields = ['email']

admin.site.register(ProductGroup, GroupsAbmin)
admin.site.register(ProductCategory, CategoriesAdmin)
admin.site.register(ProductSubCategory, SubCategoriesAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Shops, ShopsAdmin)
admin.site.register(CustomUser, UsersAdmin)
