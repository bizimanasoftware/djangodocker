# emergencies/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Import Q for complex lookups

from .models import EmergencyCampaign, PaymentMethod, SponsorMessage, CampaignComment
from .forms import (
    EmergencyCampaignRequestForm, CampaignUpdateForm, PaymentMethodForm,
    SponsorMessageForm, CampaignCommentForm
)

class EmergencyCampaignListView(ListView):
    model = EmergencyCampaign
    template_name = 'emergencies/campaign_list.html'
    context_object_name = 'campaigns'
    paginate_by = 12

    def get_queryset(self):
        """ Override to filter based on GET parameters. """
        queryset = EmergencyCampaign.objects.filter(status=EmergencyCampaign.CampaignStatus.ACTIVE)
        search_query = self.request.GET.get('q', None)
        country_filter = self.request.GET.get('country', None)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(city__icontains=search_query)
            )

        if country_filter and country_filter != 'all':
            queryset = queryset.filter(country__iexact=country_filter)

        return queryset

    def get_context_data(self, **kwargs):
        """ Add filter data to the context. """
        context = super().get_context_data(**kwargs)
        # Get a unique, sorted list of countries for the dropdown filter
        countries = EmergencyCampaign.objects.filter(status=EmergencyCampaign.CampaignStatus.ACTIVE) \
                                           .exclude(country__isnull=True).exclude(country__exact='') \
                                           .values_list('country', flat=True).distinct().order_by('country')
        context['countries'] = countries
        # Pass current filter values back to the template
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_country'] = self.request.GET.get('country', '')
        return context


class EmergencyCampaignDetailView(DetailView):
    model = EmergencyCampaign
    template_name = 'emergencies/emergency_detail.html'
    context_object_name = 'campaign'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = self.get_object()
        context['contact_form'] = SponsorMessageForm()
        context['comment_form'] = CampaignCommentForm()
        context['payment_methods'] = campaign.payment_methods.all()
        context['comments'] = campaign.comments.all().order_by('-timestamp')
        context['gallery_images'] = campaign.gallery_images.all()
        return context

class ProcessSponsorMessageView(View):
    """
    Handles the form submission for the sponsor contact form.
    """
    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        campaign = get_object_or_404(EmergencyCampaign, slug=slug)
        form = SponsorMessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.campaign = campaign
            message.save()
            messages.success(request, "Your message has been sent to the campaign creator!")
        else:
            messages.error(request, "There was an error with your form. Please check the fields and try again.")
        
        return redirect(campaign.get_absolute_url())

class AddCommentView(LoginRequiredMixin, View):
    """ Handles adding a new comment to a campaign. """
    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        campaign = get_object_or_404(EmergencyCampaign, slug=slug)
        form = CampaignCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.campaign = campaign
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment has been posted.")
        else:
            messages.error(request, "There was an error posting your comment.")
        
        return redirect(campaign.get_absolute_url())

class CreateCampaignRequestView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = EmergencyCampaign
    form_class = EmergencyCampaignRequestForm
    template_name = 'emergencies/create_campaign_request.html'
    permission_required = 'emergencies.can_request_campaign'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, "Your campaign request has been submitted for admin review.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('emergencies:dashboard')

# --- Dashboard & Campaign Management Views ---

@login_required
def dashboard_view(request):
    """
    Dashboard for users to manage their created campaigns and view messages.
    """
    user_campaigns = EmergencyCampaign.objects.filter(creator=request.user)
    
    # Mark messages as read when the dashboard is viewed
    for campaign in user_campaigns:
        for message in campaign.sponsor_messages.filter(is_read=False):
            message.is_read = True
            message.save()

    context = {
        'user_campaigns': user_campaigns,
    }
    return render(request, 'emergencies/dashboard.html', context)

class CampaignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmergencyCampaign
    form_class = CampaignUpdateForm
    template_name = 'emergencies/update_campaign.html'

    def test_func(self):
        campaign = self.get_object()
        return self.request.user == campaign.creator

    def get_success_url(self):
        messages.success(self.request, "Campaign details updated successfully.")
        return reverse('emergencies:dashboard')

class PaymentMethodCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = 'emergencies/add_payment_method.html'

    def test_func(self):
        campaign = get_object_or_404(EmergencyCampaign, slug=self.kwargs.get('slug'))
        return self.request.user == campaign.creator

    def form_valid(self, form):
        campaign = get_object_or_404(EmergencyCampaign, slug=self.kwargs.get('slug'))
        form.instance.campaign = campaign
        messages.success(self.request, "Payment method added successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('emergencies:dashboard')

class PaymentMethodDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PaymentMethod
    template_name = 'emergencies/confirm_delete_payment.html'
    
    def test_func(self):
        payment_method = self.get_object()
        return self.request.user == payment_method.campaign.creator

    def get_success_url(self):
        messages.success(self.request, "Payment method has been deleted.")
        return reverse('emergencies:dashboard')
