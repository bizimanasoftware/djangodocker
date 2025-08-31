from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    """
    The view for the comedian's dashboard.
    """
    return render(request, 'comedians/dashboard.html')
