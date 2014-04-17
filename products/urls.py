from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('products.views',

    url(r'^catalog/list/$', CatalogList.as_view(), name='catalog_list'),
    url(r'^catalog/detail/(?P<slug>\w+)/$', CatalogDetail.as_view(), name='catalog_detail'),

    url(r'^open/$', ShopCreate.as_view(), name = 'shop_create'),
    url(r'^all/$', ShopList.as_view(), name='shop_list'),
    url(r'^detail/(?P<slug>\w+)/$', ShopDetail.as_view(), name='shop_detail'),

    url(r'^product/create/$', ProductCreate.as_view(), name = 'product_create'),
    url(r'^product/list/$', ProductList.as_view(), name='product_list'),
    url(r'^product/detail/(?P<slug>[-_\w]+)/$', ProductDetail.as_view(), name='product_detail'),

    url(r'^like/$', ProductLike.as_view(), name='product_like'),



)    