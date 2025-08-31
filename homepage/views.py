from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.models import Profile, SponsorshipRequest
from emergencies.models import EmergencyCampaign

def index(request):
    # 1. Query for the latest public profiles
    latest_profiles = Profile.objects.filter(is_public=True).select_related('user').order_by('-id')[:6]

    # 2. Query for recent sponsorships
    recent_sponsorships = SponsorshipRequest.objects.select_related(
        'profile__user'
    ).filter(
        action__in=['sponsor', 'donate']
    ).order_by('-created_at')[:6]

    # 3. Query for featured campaigns
    featured_campaigns = EmergencyCampaign.objects.filter(
        status=EmergencyCampaign.CampaignStatus.ACTIVE,
        is_featured=True
    ).order_by('-start_date')[:4]

    # 4. Create a single context dictionary with all the data
    context = {
        'latest_profiles': latest_profiles,
        'recent_sponsorships': recent_sponsorships,
        'featured_campaigns': featured_campaigns,
    }

    # 5. Return a single render call with the complete context
    return render(request, 'homepage/index.html', context)


def about(request):
    return render(request, 'homepage/about.html')

def become_agent(request):
    return render(request, 'homepage/become_agent.html')

def become_talent(request):
    return render(request, 'homepage/become_talent.html')

def sponsor_donate(request):
    return render(request, 'homepage/sponsor_donate.html')

def support(request):
    return render(request, 'homepage/support.html')

def terms(request):
    return render(request, 'homepage/terms.html')
