from django.db import models
from django.core.urlresolvers import reverse_lazy as reverse
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db.models import Count
User = get_user_model()


class Catalog(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children')
    image = models.ImageField(
        verbose_name=u'Image', upload_to="category_pic", blank=True)

    def __unicode__(self):
        return self.title

    # def delete(self):
    #     super(Catalog, self).delete()

    def get_absolute_url(self):
        return reverse('catalog_detail', kwargs={'slug': self.slug})


class Shop(models.Model):
    title = models.CharField(max_length=30)
    website = models.URLField()
    avatar = models.ImageField(
        verbose_name=u'Avatar', upload_to="avatar_pic", blank=True)
    description = models.TextField(blank=True,
                                   help_text="Describe yourself.")
    submitter = models.ForeignKey(User)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'slug': self.slug})

    def likes(self):
        return Like.objects.filter(product__shop=self).count()


class ProductManager(models.Manager):

    def get_featured(self):
        return self.filter(is_featured=True)


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        verbose_name=u'Image', upload_to="product_pic", blank=True)
    catalog = models.ForeignKey(Catalog)
    description = models.TextField(blank=True, help_text="Describe product")
    submitter = models.ForeignKey(User)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=15, decimal_places=2, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shop = models.ForeignKey(Shop)

    @models.permalink
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    objects = ProductManager()

    class Meta:
        permissions = (
            ('can_like', 'Can like product'),
        )

    @models.permalink
    def like_url(self):
        return '/shop/like/?product=%s' % self.pk

    def likes(self):
        return Like.objects.aggregate(Count('likes'))

    def __unicode__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, related_name='product_likes')
    product = models.ForeignKey(Product, related_name='likes')

    class Meta:
        unique_together = (
            ('user', 'product'),
        )


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    bio = models.TextField(null=True)

    def __unicode__(self):
        return "%s's profile" % self.user


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)

# Signal while saving user
from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)
#post_save.connect(update_likes, sender=Likes)
