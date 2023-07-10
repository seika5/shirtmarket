from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item

class ItemListView(ListView):
	model = Item
	template_name = 'home.html'
	context_object_name = 'items'
	ordering = ['-date_posted']
	paginate_by = 12

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Item
	fields = ['name', 'description', 'image', 'price', 'sales_limit']
	template_name = 'item_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self): 
		if self.request.user.is_superuser:
			return True
		return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Item
	success_url = '/'
	template_name = 'item_confirm_delete.html'
	context_object_name = 'item'

	def test_func(self): 
		if self.request.user.is_superuser:
			return True
		return False

class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Item 
	fields = ['name', 'description', 'image', 'price', 'sales_limit']
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