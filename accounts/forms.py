# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, AdminUserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(AdminUserCreationForm): # Inherit from AdminUserCreationForm for admin compatibility
    """
    A form for creating new users. Includes the user_type field.
    Handles username uniqueness automatically (via UserCreationForm/AbstractUser).
    Adds custom validation for email uniqueness.
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'})
    )
    user_type = forms.ChoiceField(
        choices=CustomUser.UserType.choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_user_type'})
    )

    # --- CRITICAL CHANGE: Explicitly define password1 and password2 as form fields ---
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password1', 'autocomplete': 'new-password'}),
        label="Password" # Add a label since it's a custom field
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password2', 'autocomplete': 'new-password'}),
        label="Password (confirmation)" # Add a label
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # --- CRITICAL CHANGE: List password1 and password2 explicitly here ---
        fields = ('username', 'email', 'user_type', 'password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_username', 'autocomplete': 'username'}),
            # REMOVE password1 and password2 from here, as they are now defined directly on the form class.
            # Only include widgets for fields *not* explicitly defined as forms.Field instances.
        }
        # The UserCreationForm.Meta.widgets would typically handle password fields,
        # but since we're defining them explicitly, this 'widgets' dict should reflect that.
        # So, the 'password1' and 'password2' lines in this widgets dict should actually be removed
        # if they are defined as forms.CharField above. I've removed them from the 'Meta.widgets' for clarity.
        # This means the widget attrs are now handled directly where the fields are defined.


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if CustomUser.objects.filter(email__iexact=email).exists():
                raise ValidationError("This email address is already in use. Please use a different one.")
        return email

    def clean(self):
        # --- CRITICAL CHANGE: Handle password matching here yourself ---
        # If you define password1 and password2 fields, super().clean() might not
        # perform the matching, so you need to do it explicitly.
        
        cleaned_data = super().clean() # Call parent clean, but be aware of its password handling.
                                      # AdminUserCreationForm's clean might still look for 'password'.

        password = cleaned_data.get("password1") # Use password1 here
        password2 = cleaned_data.get("password2") # Use password2 here

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords don't match.") # Add error to password2 field

        print("\n--- Inside CustomUserCreationForm.clean() ---")
        print("Cleaned data received by form.clean():")
        print(f"  username: {cleaned_data.get('username')}")
        print(f"  email: {cleaned_data.get('email')}")
        print(f"  user_type: {cleaned_data.get('user_type')}")
        # Now correctly checking for 'password1' and 'password2' as per new field names
        print(f"  password1: {'<present>' if cleaned_data.get('password1') else '<empty>'}") 
        print(f"  password2: {'<present>' if cleaned_data.get('password2') else '<empty>'}") 

        if self.errors:
            print("Form has errors after custom and super().clean():")
            for field, errors in self.errors.items():
                print(f"  Field '{field}': {errors}")
        else:
            print("No errors detected by custom and super().clean().")

        print("--- Exiting CustomUserCreationForm.clean() ---")
        return cleaned_data

    # --- CRITICAL ADDITION: Override save method to set the password from 'password1' ---
    # This is necessary because UserCreationForm's save() expects 'password', not 'password1'.
    def save(self, commit=True):
        user = super().save(commit=False) # Call parent save to get the user instance, but don't commit yet
        password = self.cleaned_data["password1"] # Get the password from password1
        user.set_password(password) # Set the hashed password
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_login_username', 'autocomplete': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_login_password', 'autocomplete': 'current-password'}))

class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating existing users in the admin.
    Includes the user_type field.
    """
    user_type = forms.ChoiceField(
        choices=CustomUser.UserType.choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
