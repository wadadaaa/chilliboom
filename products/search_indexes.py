import datetime
from haystack import indexes
from products.models import Product, Shop


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    submitter = indexes.CharField(model_attr='submitter')
    created_at = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())