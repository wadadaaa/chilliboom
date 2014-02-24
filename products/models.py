from django.db import models
#from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from updown.fields import RatingField



try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

#import PIL
#from PIL import Image
#from easy_thumbnails.fields import ThumbnailerImageField

class Catalog(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title


class Subcatalog(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    catalog = models.ForeignKey(Catalog)

    def __unicode__(self):
        return self.title


class Shop(models.Model):
    title = models.CharField(max_length=30)
    website = models.URLField()
    avatar = models.ImageField(verbose_name=u'Avatar', upload_to="avatar_pic", blank=True)
    description = models.TextField(blank=True,
                                   help_text="Describe yourself.")
    submitter = models.ForeignKey(User)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'slug':self.slug})


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name=u'Image', upload_to="product_pic", blank=True)
    catalog = models.ForeignKey(Catalog)
    subcatalog = models.ManyToManyField(Subcatalog)
    description = models.TextField(blank=True, help_text="Describe product")
    submitter = models.ForeignKey(User)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    sale_price = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shop = models.ForeignKey(Shop)
    rating = RatingField()
    

    def __unicode__(self):
        return self.title



class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    bio = models.TextField(null=True)

    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

# Signal while saving user
from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)
