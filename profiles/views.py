# /home/deploy/gloexproject/profiles/views.py
# Contains the business logic for handling requests and serving responses.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Profile, ProfileGallery, SponsorshipRequest, ProfileComment
from .forms import (
    ProfileForm, ProfileGalleryFormSet, SponsorshipRequestForm, ProfileCommentForm,
    PaymentLinkFormSet, CryptoWalletFormSet
)

@login_required
def dashboard(request):
    """ Main dashboard view for a logged-in user. """
    profile, created = Profile.objects.get_or_create(user=request.user)
    requests = SponsorshipRequest.objects.filter(profile=profile).order_by('-created_at')[:10]
    context = {'profile': profile, 'requests': requests}
    return render(request, 'dashboards/dashboard.html', context)

@login_required
def edit_profile(request):
    """ View for editing the user's profile, including payment and crypto links. """
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Bind the forms to the POST data
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        payment_formset = PaymentLinkFormSet(request.POST, instance=profile)
        crypto_formset = CryptoWalletFormSet(request.POST, instance=profile)

        # Validate all forms at once
        if form.is_valid() and payment_formset.is_valid() and crypto_formset.is_valid():
            form.save()
            payment_formset.save()
            crypto_formset.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profiles:dashboard')
    else:
        # Create unbound forms for GET request
        form = ProfileForm(instance=profile)
        payment_formset = PaymentLinkFormSet(instance=profile)
        crypto_formset = CryptoWalletFormSet(instance=profile)
        
    context = {
        'form': form,
        'payment_formset': payment_formset,
        'crypto_formset': crypto_formset
    }
    return render(request, 'profiles/edit_profile.html', context)

@login_required
def manage_gallery(request):
    # This view remains unchanged
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        formset = ProfileGalleryFormSet(request.POST, request.FILES, queryset=ProfileGallery.objects.filter(profile=profile))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances: instance.profile = profile; instance.save()
            for obj in formset.deleted_objects: obj.delete()
            messages.success(request, 'Gallery updated successfully!')
            return redirect('profiles:manage_gallery')
    else:
        formset = ProfileGalleryFormSet(queryset=ProfileGallery.objects.filter(profile=profile))
    current_images_count = ProfileGallery.objects.filter(profile=profile).count()
    remaining_slots = 20 - current_images_count
    context = {'formset': formset, 'profile': profile, 'remaining_slots': remaining_slots}
    return render(request, 'profiles/manage_gallery.html', context)

def discover_profiles(request):
    """ Public view to discover profiles, with search and filtering. """
    profiles_list = Profile.objects.filter(is_public=True).select_related('user').order_by('user__username')
    query = request.GET.get('q')
    category = request.GET.get('category')

    if category and category != 'all':
        profiles_list = profiles_list.filter(category__iexact=category)

    if query:
        profiles_list = profiles_list.filter(
            Q(user__username__icontains=query) | Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) | Q(headline__icontains=query) |
            Q(bio__icontains=query) | Q(category__icontains=query) |
            Q(city__icontains=query) | Q(country__icontains=query)
        )

    categories = Profile.objects.filter(is_public=True).values_list('category', flat=True).distinct()
    paginator = Paginator(profiles_list, 24)
    page_number = request.GET.get('page')
    profiles = paginator.get_page(page_number)

    context = {
        'profiles': profiles, 'categories': categories,
        'selected_category': category, 'search_query': query,
    }
    return render(request, 'discover.html', context)

def profile_detail(request, pk):
    """ Public detail view for a single profile, displaying approved comments. """
    profile = get_object_or_404(Profile, pk=pk, is_public=True)
    gallery_images = profile.gallery_images.filter(is_public=True)
    comments = profile.comments.filter(is_approved=True) # Only show approved comments
    comment_form = ProfileCommentForm()
    
    context = {
        'profile': profile, 'gallery_images': gallery_images,
        'comments': comments, 'comment_form': comment_form,
    }
    return render(request, 'profiles/profile_detail.html', context)

def add_comment(request, pk):
    """ Handles submission of a new comment for moderation. """
    profile = get_object_or_404(Profile, pk=pk, is_public=True)
    if request.method == 'POST':
        form = ProfileCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.profile = profile
            comment.save() # is_approved is False by default
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
        else:
            messages.error(request, 'There was an error with your submission.')
    return redirect('profiles:profile_detail', pk=profile.pk)

@user_passes_test(lambda u: u.is_superuser)
def delete_comment(request, comment_id):
    """ Allows a superuser to delete a comment. """
    comment = get_object_or_404(ProfileComment, id=comment_id)
    profile_pk = comment.profile.pk # Get profile ID before deleting
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    return redirect('profiles:profile_detail', pk=profile_pk)

def sponsorship_request_view(request, pk, action):
    # This view remains unchanged
    profile = get_object_or_404(Profile, pk=pk, is_public=True)
    if action not in ['sponsor', 'donate', 'connect', 'hire']:
        messages.error(request, 'Invalid action.')
        return redirect('profiles:profile_detail', pk=profile.pk)
    if request.method == 'POST':
        form = SponsorshipRequestForm(request.POST)
        if form.is_valid():
            sponsorship_request = form.save(commit=False)
            sponsorship_request.profile = profile; sponsorship_request.action = action
            sponsorship_request.save()
            return redirect('profiles:request_submitted', pk=profile.pk)
    else:
        form = SponsorshipRequestForm()
    context = {'form': form, 'profile': profile, 'action': action.capitalize()}
    return render(request, 'profiles/sponsorship_request_form.html', context)

def request_submitted(request, pk):
    # This view remains unchanged
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'profiles/request_submitted.html', {'profile': profile})
