# settingspanel/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def settings_home(request):
    """
    Displays the main settings page.
    """
    return render(request, 'settingspanel/settings_home.html')
