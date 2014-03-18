from django.db import models
from django.core.urlresolvers import reverse_lazy as reverse
from django.utils.timezone import now
from django.contrib.auth import get_user_model
User = get_user_model()


class Catalog(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    image = models.ImageField(verbose_name=u'Image', upload_to="category_pic", blank=True)
    
    def __unicode__(self):
        return self.title

    # def delete(self):
    #     super(Catalog, self).delete()

    def get_absolute_url(self):
        return reverse('catalog_detail', kwargs={'slug': self.slug})


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
        return reverse('shop_detail', kwargs={'slug': self.slug})


class ProductManager(models.Manager):
    def get_featured(self):
        return self.filter(is_featured=True)

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name=u'Image', upload_to="product_pic", blank=True)
    catalog = models.ForeignKey(Catalog)
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
    #likes = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


    objects = ProductManager()
    

    def __unicode__(self):
        return self.title



'''
def update_likes(sender, instance, updated, **kwargs):
    if updated:
        likes+=1 #i have no
'''


'''
class Likes(models.Model):
    submitter = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (('submitter', 'product', 'created_at'))

    def __unicode__(self):
        return "%s submitter is like %s" % (self.submitter, self.product)

    def save(self, *args, **kwargs):
        self.created_at = now()
        super(Like, self).save(*args, **kwargs)

'''

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
