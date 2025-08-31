from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    """
    The view for the 'other' user's dashboard.
    """
    return render(request, 'others/dashboard.html')
