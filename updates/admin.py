# updates/admin.py

from django.contrib import admin
from .models import Post, Category, PostImage

# NEW: Inline admin for the gallery images
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1  # Show one extra empty slot for a new image
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # This is for showing a small preview in the admin
        from django.utils.html import mark_safe
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return ""


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # ... (no changes here)
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_at')
    list_filter = ('status', 'category', 'created_at', 'published_at')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ('status', '-published_at')

    # ADDED: The new image gallery inline
    inlines = [PostImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('body', 'featured_image', 'featured_video', 'attachment')
        }),
        ('Styling', {
            'classes': ('collapse',), 
            'fields': ('title_color', 'font_size', 'underline_title')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at')
        }),
    )
