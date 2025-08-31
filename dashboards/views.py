from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser

@login_required
def dashboard_redirect_view(request):
    """
    This is the core of the redirection logic.
    It checks the user's 'user_type' and redirects them to the
    appropriate app's dashboard.
    """
    user = request.user
    
    if user.user_type == CustomUser.UserType.ARTIST:
        # Redirect to the URL named 'dashboard' inside the 'artists' app
        return redirect('artists:dashboard')
        
    elif user.user_type == CustomUser.UserType.FOOTBALLER:
        # Redirect to the URL named 'dashboard' inside the 'footballers' app
        return redirect('footballers:dashboard')
    elif user.user_type == CustomUser.UserType.AGENT:
        # Redirect to the URL named 'dashboard' inside the 'footballers' app
        return redirect('agents:dashboard')
    elif user.user_type == CustomUser.UserType.SPONSOR:
        # Redirect to the URL named 'dashboard' inside the 'footballers' app
        return redirect('sponsors:dashboard')
    elif user.user_type == CustomUser.UserType.EMERGENCY:
        # Redirect to the URL named 'dashboard' inside the 'footballers' app
        return redirect('emergencies:dashboard')
    elif user.user_type == CustomUser.UserType.EMPLOYER:
        # Redirect to the URL named 'dashboard' inside the 'footballers' app
        return redirect('employers:dashboard')
    elif user.user_type == CustomUser.UserType.CODER:
        # Redirect to the URL named 'dashboard' inside the 'footballers' app
        return redirect('coders:dashboard')
    elif user.user_type == CustomUser.UserType.INFLUENCER:
        return redirect('influencers:dashboard')
    elif user.user_type == CustomUser.UserType.FILMMAKER:
        return redirect('filmmakers:dashboard')
    elif user.user_type == CustomUser.UserType.COMEDIAN:
        return redirect('comedians:dashboard')
    elif user.user_type == CustomUser.UserType.VOLLEYBALLER:
        return redirect('volleyballers:dashboard')
    elif user.user_type == CustomUser.UserType.VOLUNTEER:
        return redirect('volunteers:dashboard')
    elif user.user_type == CustomUser.UserType.JOURNALIST:
        return redirect('journalists:dashboard')
    elif user.user_type == CustomUser.UserType.TRADER:
        return redirect('traders:dashboard')
    elif user.user_type == CustomUser.UserType.BOXER:
        return redirect('boxers:dashboard')
    elif user.user_type == CustomUser.UserType.DONOR:
        return redirect('donors:dashboard')
    elif user.user_type == CustomUser.UserType.OTHER:
        return redirect('others:dashboard')
        
    # Add more conditions for other user types here
    # elif user.user_type == CustomUser.UserType.AGENT:
    #     return redirect('agents:dashboard')
    
    else:
        # Fallback for any other user type or if something is wrong.
        # You could create a generic dashboard for this.
        # For now, we redirect to the homepage.
        return redirect('homepage:index')

