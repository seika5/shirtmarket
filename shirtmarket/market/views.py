from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView
from .models import Item

class ItemListView(ListView):
	model = Item
	template_name = 'home.html'
	context_object_name = 'items'
	ordering = ['-date_posted']
	paginate_by = 12

"""
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post 
	fields = ['title', 'content']
	template_name = 'post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self): 
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post 
	success_url = '/'
	template_name = 'post_confirm_delete.html'
	context_object_name = 'post'

	def test_func(self): 
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
"""

class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Item 
	fields = ['name', 'description', 'image', 'price']
	template_name = 'item_form.html'

	def test_func(self): 
		if self.request.user.is_superuser:
			return True
		return False

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class ItemDetailView(DetailView):
	model = Item 
	template_name = 'item_detail.html'
	context_object_name = 'item'

def about(request):
	return render(request, 'about.html', {'title': 'About'})