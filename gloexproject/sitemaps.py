# gloexproject/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# Import your dynamic models here to generate sitemaps from them
from profiles.models import Profile
# Assuming you have models for EmergencyCampaigns and Updates
from emergencies.models import EmergencyCampaign
from updates.models import Post

class StaticSitemap(Sitemap):
    """
    Sitemap for all your static pages.
    """
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        """
        Returns a list of URL names for all your static pages.
        Each name must be in the format 'app_name:url_name'.
        """
        return [
            # Homepage app URLs
            'homepage:index',
            'homepage:become_agent',
            'homepage:become_talent',
            'homepage:sponsor_donate',
            'homepage:terms',

            # Accounts app URLs
            'accounts:unified_auth',
            'accounts:register',
            'accounts:login',
            'accounts:logout',

            # Profiles app URLs
            'profiles:discover_profiles',

            # Wallet app URLs
            'wallet:wallet_dashboard',

            # Emergencies app URLs
            'emergencies:campaign_list',
            'emergencies:create_campaign_request',
            'emergencies:donation_success',
            'emergencies:dashboard',

            # Updates app URLs
            'updates:post_list',
            'updates:admin_post_list',
        ]

    def location(self, item):
        """
        The location method uses the URL name to get the full URL.
        """
        return reverse(item)


class ProfileSitemap(Sitemap):
    """
    Sitemap for dynamic profile pages.
    """
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        """
        Returns all the Profile objects from the database that are public.
        """
        return Profile.objects.filter(is_public=True)

    def lastmod(self, obj):
        """
        Sets the last modified date for each profile.
        We are using the user's registration date as a substitute.
        """
        return obj.user.date_joined

    def location(self, obj):
        """
        Generates the URL for each profile using its primary key (pk).
        """
        return reverse('profiles:profile_detail', args=[obj.pk])


class EmergencySitemap(Sitemap):
    """
    Sitemap for dynamic emergency campaign pages.
    """
    changefreq = "daily"
    priority = 0.7

    def items(self):
        """
        Returns all the EmergencyCampaign objects from the database.
        """
        return EmergencyCampaign.objects.all()

    def lastmod(self, obj):
        """
        Sets the last modified date for each campaign.
        Assuming your model has a 'updated_at' or 'created_at' field.
        """
        return obj.updated_at

    def location(self, obj):
        """
        Generates the URL for each campaign using its slug.
        """
        return reverse('emergencies:campaign_detail', args=[obj.slug])


class UpdatesSitemap(Sitemap):
    """
    Sitemap for blog posts or updates.
    """
    changefreq = "daily"
    priority = 0.7

    def items(self):
        """
        Returns all the Post objects from the database.
        """
        return Post.objects.all()

    def lastmod(self, obj):
        """
        Sets the last modified date for each post.
        Assuming your model has a 'updated_at' field.
        """
        return obj.updated_at

    def location(self, obj):
        """
        Generates the URL for each post using its date and slug.
        """
        return reverse('updates:post_detail', args=[obj.pub_date.year, obj.pub_date.month, obj.pub_date.day, obj.slug])
