from django import forms
from haystack.forms import SearchForm


class ProductSearchForm(SearchForm):
    
    def search(self):
        return pass

       