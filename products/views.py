from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from .models import UserProfile
from .models import Product
from .models import Shop
from .models import Catalog
from .models import Subcatalog
from .forms import UserProfileForm, ProductForm, OpenShopForm, AddproductForm





class ProductListView(ListView):
    model = Product

class CatalogView(ListView):
    model = Catalog

class SubcatalogView(ListView):
    model = Subcatalog

class ShopListView(ListView):
    model = Shop





class ShopView(DetailView):
    model = Shop
    products = Product.objects.filter(shop=Shop)
    template_name = "products/shop_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        return context


class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.submitter = self.request.user
        f.save()

        return super(CreateView, self).form_valid(form)

class OpenShop(CreateView):
    model = Shop
    form_class = OpenShopForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.submitter = self.request.user
        f.save()
        return super(OpenShop, self).form_valid(form)
    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


class AddProduct(CreateView):
    model = Product
    form_class = AddproductForm

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super(AddProduct, self).form_valid(form)
    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})




