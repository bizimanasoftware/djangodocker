from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def donate(request):
    return render(request, "sponsor_donate/donate.html")

@login_required
def my_donations(request):
    return render(request, "sponsor_donate/my_donations.html")
