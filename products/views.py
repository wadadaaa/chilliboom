from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
User = get_user_model()


from products.models import (
    Profile,
    Product,
    Shop,
    Catalog,
    #Likes,

)
from products.forms import (
    ProfileForm,
    ShopCreateForm,
    ProductCreateForm
)


#TODO: pagination for all lists


class ProductMixin(object):
    model = Product


class ProductDetail(ProductMixin, DetailView):
    pass


class ProductList(ProductMixin, ListView):
    pass


class ProductCreate(ProductMixin, SuccessMessageMixin, CreateView):
    form_class = ProductCreateForm
    success_message = "New product added"

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super(ProductCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


class CatalogMixin(object):
    model = Catalog


class CatalogList(CatalogMixin, ListView):
    pass


class CatalogDetail(CatalogMixin, DetailView):
    
    def get_context_data(self, **kwargs):
        context = super(CatalogDetail, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(catalog=Catalog)

        return context



class ShopMixin(object):
    model = Shop


class ShopList(ShopMixin, ListView):
    pass


class ShopDetail(ShopMixin, DetailView):
    products = Product.objects.filter(shop=Shop)

    def get_context_data(self, **kwargs):
        context = super(ShopDetail, self).get_context_data(**kwargs)
        return context


class ShopCreate(ShopMixin, SuccessMessageMixin, CreateView):
    form_class = ShopCreateForm
    success_message = "You opened own shop!"

    def form_valid(self, form):
        f = form.save(commit=False)
        f.submitter = self.request.user
        
        f.save()
        return super(ShopCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


class ProfileDetail(DetailView):
    model = User
    slug_field = "username"

    def get_object(self, queryset=None):
        user = super(ProfileDetail, self).get_object(queryset)
        Profile.objects.get_or_create(user=user)
        return user


class ProfileUpdate(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_message = "Profile saved"

    def get_object(self, queryset=None):
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


'''
class LikesView(CreateView):
    model = Likes
'''