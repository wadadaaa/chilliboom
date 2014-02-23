from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required as auth
from products.views import *


urlpatterns = patterns('products.views',
    url(r'^product/create/$', auth(ProductCreateView.as_view()), name='link_create'),
    url(r'^openshop/$', auth(OpenShop.as_view()), name = 'openshop'),
    url(r'^addproduct/$', auth(AddProduct.as_view()), name = 'addproduct'),
    url(r'^$', ProductListView.as_view(), name='home'),

    url(r'^detail/(?P<slug>\w+)/$', ShopView.as_view(), name="shop_detail"),
    url(r'^catalogs/$', CatalogView.as_view(), name="catalog_list"),
    url(r'^list/$', ShopListView.as_view(), name="shop_list"),

)    