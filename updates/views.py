# updates/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category
from .forms import PostForm

# --- Public Views ---

class PostListView(ListView):
    model = Post
    template_name = 'updates/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.kwargs.get('category_slug')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'updates/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        # Allow viewing of published posts only
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

# --- Admin Management Views ---

class IsAdminMixin(UserPassesTestMixin):
    """Mixin to ensure the user is a staff member or superuser."""
    def test_func(self):
        return self.request.user.is_staff

class AdminPostListView(LoginRequiredMixin, IsAdminMixin, ListView):
    model = Post
    template_name = 'updates/admin_post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostCreateView(LoginRequiredMixin, IsAdminMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'updates/post_form.html'
    success_url = reverse_lazy('updates:admin_post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, IsAdminMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'updates/post_form.html'
    success_url = reverse_lazy('updates:admin_post_list')

class PostDeleteView(LoginRequiredMixin, IsAdminMixin, DeleteView):
    model = Post
    template_name = 'updates/post_confirm_delete.html'
    success_url = reverse_lazy('updates:admin_post_list')
