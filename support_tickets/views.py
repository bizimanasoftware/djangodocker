from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def create_ticket(request):
    return render(request, "support_tickets/create_ticket.html")
