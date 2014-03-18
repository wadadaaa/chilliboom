__author__ = 'annalopatinski'

from django.contrib import admin
from django.conf import settings
from products.models import (
    Product,
    Catalog,
    Profile,
    Shop
)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('admin_thumbnail', 'title', 'is_featured')
    list_filter = ('created_at', 'is_featured')

    def admin_thumbnail(self, obj):
    	return '<img src="%s%s" alt="" height="50">'  % (settings.MEDIA_URL, obj.image)
    admin_thumbnail.allow_tags = True    


class CatalogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('admin_thumbnail', 'title')

    def admin_thumbnail(self, obj):
        return '<img src="%s%s" alt="" height="50">'  % (settings.MEDIA_URL, obj.image)
    admin_thumbnail.allow_tags = True


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ProfileAdmin(UserAdmin):
    inlines=(ProfileInline, )


class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('admin_thumbnail', 'title')
    list_filter = ('created_at',)

    def admin_thumbnail(self, obj):
        return '<img src="%s%s" alt="" height="50">'  % (settings.MEDIA_URL, obj.avatar)
    admin_thumbnail.allow_tags = True    


admin.site.register(Product, ProductAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
admin.site.register(Shop,ShopAdmin)