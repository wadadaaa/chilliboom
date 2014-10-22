from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from products.views import ProfileDetail, ProfileUpdate
from django.contrib.auth.decorators import login_required as auth

admin.autodiscover()


urlpatterns = patterns('',

                       url(r'^administration/', include(admin.site.urls)),

                       url(r'^$', TemplateView.as_view(
                           template_name='home.html'), name='home'),
                       # url(r'^login/$', 'django.contrib.auth.views.login',
                       #     {'template_name': 'registration/login.html'}, name="shop_login"),
                       # url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
                       #     name="shop_logout"),
                       # url(r'^accounts/', include(
                       #     'registration.backends.default.urls')),
                       url(r'^account/', include('allauth.urls')),
                       url(r'^users/(?P<slug>\w+)/$',
                           ProfileDetail.as_view(), name="profile"),
                       url(r'^profile/edit/$',
                           auth(ProfileUpdate.as_view()), name="profile_edit"),

                       url(r'^shop/', include('products.urls')),
                       url(r'^search/', include('haystack.urls')),

                       )

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
