"""gloexproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap  # You will create this file in the next step
from emails.views import email_composer_view # Import the composer view
sitemaps = {
    'static': StaticSitemap,
    # Add other sitemaps for your models here
}



admin.site.site_header = "Gloex Administration"
admin.site.site_title = "Gloex Administration Portal"
admin.site.index_title = "Welcome to the Gloex Administration"

def offline_view(request):
    return render(request, 'offline.html')

urlpatterns = [
    path('admin/emails/composer/', email_composer_view, name='admin_email_composer'), # Custom admin view
    path('admin/', admin.site.urls),
    # This makes the homepage app's URLs the root of the site.
    path('', include(('homepage.urls', 'homepage'), namespace='homepage')),
    path('offline/', offline_view, name='offline'),
    # URLs for user authentication (login, register, logout)
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # URL for the main dashboard redirector
    path('dashboard/', include(('dashboards.urls', 'dashboards'), namespace='dashboards')),

    # URLs for the specific user dashboards
    path('artist/', include(('artists.urls', 'artists'), namespace='artists')),
    path('footballer/', include(('footballers.urls', 'footballers'), namespace='footballers')),
    path('agent/', include(('agents.urls','agents'), namespace='agents')),
    path('sponsor/', include(('sponsors.urls','sponsors'), namespace='sponsors')),
    path('wallet/', include(('wallet.urls','wallet'), namespace='wallet')),
    path('emergencies/', include(('emergencies.urls', 'emergencies'), namespace='emergencies')),
    path('employer/', include(('employers.urls', 'employers'), namespace='employers')),
    path('coder/', include(('coders.urls', 'coders'), namespace='coders')),
    path('influencer/', include(('influencers.urls', 'influencers'), namespace='influencers')),
    path('filmmaker/', include(('filmmakers.urls', 'filmmakers'), namespace='filmmakers')),
    path('comedian/', include(('comedians.urls', 'comedians'), namespace='comedians')),
    path('volleyballer/', include(('volleyballers.urls', 'volleyballers'), namespace='volleyballers')),
    path('volunteer/', include(('volunteers.urls', 'volunteers'), namespace='volunteers')),
    path('journalist/', include(('journalists.urls', 'journalists'), namespace='journalists')),
    path('trader/', include(('traders.urls', 'traders'), namespace='traders')),
    path('boxer/', include(('boxers.urls', 'boxers'), namespace='boxers')),
    path('donor/', include(('donors.urls', 'donors'), namespace='donors')),
    path('other/', include(('others.urls', 'others'), namespace='others')),
    path('messages/', include('messaging.urls', namespace='messaging')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('chat/', include('chat_with_admin.urls', namespace='chat_with_admin')),
    path('updates/', include('updates.urls', namespace='updates')),
    # Add this line for the editor's image uploader
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('emails/', include('emails.urls', namespace='emails')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
