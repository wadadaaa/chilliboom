from django.views.generic import View, ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from braces.views import JSONResponseMixin, LoginRequiredMixin, PermissionRequiredMixin, AjaxResponseMixin


User = get_user_model()


from products.models import (
    Profile,
    Product,
    Shop,
    Catalog,
    Like,

)
from products.forms import (
    ProfileForm,
    ShopCreateForm,
    ProductCreateForm
)


class ProductMixin(object):
    model = Product


class ProductDetail(ProductMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        return context


class ProductList(ProductMixin, ListView):
    paginate_by = 5

DIRECTION_WEIGHT = {
    'up': 1,
}


class LikeProductMixin(SingleObjectMixin):
    model = Product

    def get_object(self, queryset=None):
        self.product = super(LikeProductMixin, self).get_object(queryset)
        try:
            obj = self.product.get(pk=self.kwargs['product_id'])
        except ObjectDoesNotExist:
            raise Http404
        return obj


# class ProductLike(LikeProductMixin, View, PermissionRequiredMixin):
#     permission_required = 'products.can_like'
#     def get(self, request, direction, weight=1):
#         self.object = self.get_object()
#         weight = DIRECTION_WEIGHT[direction] * weight
#
#         like, created = Like.objects.get_or_create(
#             user=request.user,
#             product=self.object,
#             defaults={'weight': weight}
#         )
#
#         if not created:
#             if like.weight == weight:
#
# Liked the same
#                 pass
#             elif abs(like.weight) == abs(weight):
# Liked opposite
#                 like.delete()
#             else:
#                 like.weight = weight
#                 like.save()
#         return HttpResponseRedirect(self.product.like_url())

class ProductLike(JSONResponseMixin, AjaxResponseMixin, View, PermissionRequiredMixin, LikeProductMixin):
    permission_required = 'product.can_like'

    def ok_or_bad(self):
        return 'I dunno yet'
    #
    # def get(self, request):
    #     product = request.GET['product']
    #     like = Like.objects.get_or_create(
    #         user=request.user,
    #         product=product,
    #     )
    #     like.save()

    def get_ajax(self, request, *args, **kwargs):
        json_dict = {
            'result': self.ok_or_bad
        }
        return self.render_json_response(json_dict)


class ProductCreate(ProductMixin, SuccessMessageMixin, CreateView, LoginRequiredMixin):
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


class ShopCreate(ShopMixin, SuccessMessageMixin, CreateView, LoginRequiredMixin):
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


class ProfileUpdate(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = ProfileForm
    success_message = "Profile saved"

    def get_object(self, queryset=None):
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})
