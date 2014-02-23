__author__ = 'annalopatinski'

from django.contrib import admin
from .models import Product
from .models import Catalog
from .models import Subcatalog
from .models import UserProfile
from .models import Shop

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CatalogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class SubcatalogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline, )

class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Subcatalog, SubcatalogAdmin)
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)
admin.site.register(Shop,ShopAdmin)