# agents/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    """
    The view for the agent's specific dashboard.
    """
    return render(request, 'agents/dashboard.html')
