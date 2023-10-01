from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import (
    Product,
    Shops,
    Sales,
    DataPoint
)
from users.models import CustomUser
from users.admin_forms import UserChangeForm, UserCreationForm

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


class SalesAdmin(admin.ModelAdmin):
    list_display = ("store", "SKU")

class UsersAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'password', 'is_superuser')
    list_filter = ('email',)
    search_fields = ['email']
    ordering = ('email',)
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password"],
            },
        ),
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Shops, ShopsAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(CustomUser, UsersAdmin)
admin.site.register(DataPoint)
