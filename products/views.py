from django.views.generic import ListView, DetailView, UpdateView, CreateView
#from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin


from products.models import (
    UserProfile,
    Product,
    Shop,
    Catalog,
    Subcatalog
)
from products.forms import (
    UserProfileForm,
    ProductForm,
    OpenShopForm,
    AddproductForm
)

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()



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

class UserProfileEditView(SuccessMessageMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"
    success_message = "Profile saved"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})

class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_message = "Product created"

    def form_valid(self, form):
        f = form.save(commit=False)
        f.submitter = self.request.user
        f.save()

        return super(CreateView, self).form_valid(form)

class OpenShop(SuccessMessageMixin,CreateView):
    model = Shop
    form_class = OpenShopForm
    success_message = "You opened own shop!"

    def form_valid(self, form):
        f = form.save(commit=False)
        f.submitter = self.request.user
        f.save()
        return super(OpenShop, self).form_valid(form)
    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


class AddProduct(SuccessMessageMixin,CreateView):
    model = Product
    form_class = AddproductForm
    success_message = "New product added"

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super(AddProduct, self).form_valid(form)
    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


