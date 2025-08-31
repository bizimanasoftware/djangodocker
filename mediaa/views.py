from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def upload_media(request):
    return render(request, "media/upload.html")
