# accounts/views.py
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic import View, FormView
from django.contrib import messages # Already imported, good!
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, CustomAuthenticationForm

User = get_user_model() # Get your custom user model

class UnifiedAuthView(View):
    template_name = 'accounts/unified_auth.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # When a user is already logged in and tries to access unified_auth,
            # redirect them to their dashboard. This is good practice.
            return redirect(request.user.get_dashboard_url()) # Using the new model method

        registration_form = CustomUserCreationForm()
        login_form = CustomAuthenticationForm()
        return render(request, self.template_name, {
            'registration_form': registration_form,
            'login_form': login_form,
            'active_tab': 'login-pane'
        })


class RegistrationView(FormView):
    template_name = 'accounts/unified_auth.html'
    form_class = CustomUserCreationForm
    # After successful registration, typically you'd redirect to the dashboard
    # or a "registration successful" page. If you auto-login, redirect to dashboard.
    # If not auto-logging in, redirect to unified_auth with success message.
    # Since you are auto-logging, let's make it dynamic to the user's dashboard.
    # We'll override get_success_url or directly redirect in form_valid.

    def form_valid(self, form):
        print("\n--- Inside RegistrationView.form_valid ---")
        print("Form is valid according to Django. Cleaned data:")
        print(f"  username: {form.cleaned_data.get('username')}")
        print(f"  email: {form.cleaned_data.get('email')}")
        print(f"  user_type: {form.cleaned_data.get('user_type')}")

        try:
            user = form.save()
            print(f"User '{user.username}' saved successfully in the database.")
            if user is not None:
                login(self.request, user) # Auto-login the user after successful registration
                print("User logged in.")
                
                # --- ADDED/MODIFIED SUCCESS MESSAGE HERE ---
                messages.success(self.request, f'Welcome, {user.username}! Your account has been successfully created and you are now logged in.')
                
                # Redirect to the user's specific dashboard
                return redirect(user.get_dashboard_url())
            else:
                print("form.save() unexpectedly returned None.")
                messages.error(self.request, "Account creation failed unexpectedly.")
                # If save returns None, it implies an issue before login
                login_form = CustomAuthenticationForm()
                return render(self.request, self.template_name, {
                    'registration_form': form,
                    'login_form': login_form,
                    'active_tab': 'register-pane'
                })
        except Exception as e:
            print(f"--- ERROR during form.save() or login: {e} ---")
            messages.error(self.request, f"An unexpected error occurred during registration. Please try again.")
            # Ensure forms are passed back to the template if an error occurs during save/login
            login_form = CustomAuthenticationForm()
            return render(self.request, self.template_name, {
                'registration_form': form,
                'login_form': login_form,
                'active_tab': 'register-pane'
            })


    def form_invalid(self, form):
        print("\n--- Inside RegistrationView.form_invalid ---")
        print("Form is NOT valid. Errors received by form_invalid:")
        for field, errors in form.errors.items():
            print(f"  Field '{field}': {errors}")
        if form.non_field_errors():
            print(f"  Non-field errors: {form.non_field_errors()}")

        login_form = CustomAuthenticationForm()
        # Add a general error message for invalid registration attempts
        messages.error(self.request, "Registration failed. Please correct the errors below and try again.")
        return render(self.request, self.template_name, {
            'registration_form': form,
            'login_form': login_form,
            'active_tab': 'register-pane'
        })

class CustomLoginView(LoginView):
    template_name = 'accounts/unified_auth.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        # Redirect authenticated users to their specific dashboard
        return self.request.user.get_dashboard_url()

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        response = super().form_valid(form)
        # Add a success message after a valid login
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return response

    def form_invalid(self, form):
        registration_form = CustomUserCreationForm()
        messages.error(self.request, "Login failed. Please check your username and password.")
        return render(self.request, self.template_name, {
            'login_form': form,
            'registration_form': registration_form,
            'active_tab': 'login-pane'
        })

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.") # More specific message
    return redirect('accounts:unified_auth')

@require_POST
def check_username_exists(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        is_taken = User.objects.filter(username__iexact=username).exists()
        return JsonResponse({'is_taken': is_taken})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Error in check_username_exists: {e}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@require_POST
def check_email_exists(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        is_taken = User.objects.filter(email__iexact=email).exists()
        return JsonResponse({'is_taken': is_taken})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Error in check_email_exists: {e}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)
