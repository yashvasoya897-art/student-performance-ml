from django.contrib.sitemaps.views import sitemap
from predictor.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns += [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
]
