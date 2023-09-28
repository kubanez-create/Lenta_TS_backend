from django.contrib import admin

from .models import (
    Product,
    Shops
)
from users.models import CustomUser


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


admin.site.register(Product, ProductAdmin)
admin.site.register(Shops, ShopsAdmin)
admin.site.register(CustomUser, UsersAdmin)
