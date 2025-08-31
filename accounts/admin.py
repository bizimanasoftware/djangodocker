# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm 

@admin.register(CustomUser) 
class CustomUserAdmin(UserAdmin):
    """
    Custom UserAdmin for CustomUser model.
    Overrides default forms and fieldsets to include 'user_type' and handle CustomUser fields.
    """
    form = CustomUserChangeForm 
    add_form = CustomUserCreationForm 

    model = CustomUser

    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active') 
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_type')

    fieldsets = (
        (None, {'fields': ('username', 'password')}), 
        ('Personal info', {'fields': ('email', 'user_type')}), 
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # --- CRITICAL CHANGE: Use 'password1' and 'password2' in add_fieldsets ---
    # This must match the explicit field names in CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'password1', 'password2'), 
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'POST':
            form = self.add_form(request.POST) 
            if not form.is_valid():
                print("\n--- ADMIN ADD USER FORM ERRORS (add_view) ---")
                print(form.errors)
                print("--- END ADMIN ADD USER FORM ERRORS ---")
        return super().add_view(request, form_url, extra_context)
