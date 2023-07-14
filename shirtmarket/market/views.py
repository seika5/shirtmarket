from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from .models import Item
import stripe

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

def purchaseSuccess(request):
    return render(request, 'purchase_success.html')

def about(request):
	return render(request, 'about.html', {'title': 'About'})

@csrf_exempt
def stripe_config(request):
	if request.method == 'GET':
		stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
		return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request, pk):
	item = Item.objects.get(id=pk)
	if request.method == 'GET':
		domain_url = "http://localhost:8000/"
		stripe.api_key = settings.STRIPE_SECRET_KEY
		try:
			checkout_session = stripe.checkout.Session.create(
				success_url = domain_url + "success",
				cancel_url = domain_url + "item/" + str(pk),
				payment_method_types=['card'],
				mode='payment',
				line_items=[
					{
						'price_data': {
							'currency': 'usd',
							'product_data': {
								'name': item.name,
							},
							'unit_amount': item.price,
						},
						'quantity': 1,
					}
				]
			)
			return JsonResponse({'sessionId': checkout_session['id']})
		except Exception as e:
			return JsonResponse({'error': str(e)})