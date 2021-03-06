def featured_liked(request):
	from products.models import Product, Catalog
	from django.conf import settings
	featured_liked = {
	    'featured_products': Product.objects.get_featured().select_related()[:getattr(settings, 'PRODUCT_FEATURED_COUNT', 10)],
	    'catalogs': Catalog.objects.all()
	}
	return featured_liked

def search_form(request):
    from haystack.forms import ModelSearchForm
    haystack_form = {
        'haystack_form': ModelSearchForm
    }
    return haystack_form