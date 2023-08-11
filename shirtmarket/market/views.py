import datetime

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.db.models import Count
from .models import Item, Category, Order
from .forms import ContactForm
import stripe, time

class LandingView(ListView):
	model = Item
	template_name = 'home.html'

	def get_context_data(self, *args, **kwargs):
		favorites = Item.objects.annotate(fav=Count('favorites')).order_by('-fav')
		category = Category.objects.latest('id')
		items = Item.objects.filter(category=category)
		items = items.annotate(num_fav=Count('favorites'))
		items = items.order_by('-num_fav')
		context = {
			'most_liked': favorites.filter()[:2],
			'items': items.filter()[:4],
			'category': category.name,
		}
		return context

class ItemListView(ListView):
	model = Item
	template_name = 'store.html'
	paginate_by = 12

	def get_queryset(self):
		items = Item.objects.all().order_by('-date_posted')
		return items

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all().order_by('-date_posted')
		return context

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Item
	fields = ['name', 'description', 'image', 'price', 'sales_limit', 'category']
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
	fields = ['name', 'description', 'image', 'price', 'sales_limit', 'expire_date', 'category']
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

	def get_context_data(self, *args, **kwargs):
		item = Item.objects.get(id=self.kwargs.get('pk'))
		if item.expire_date:
			context = {
				'item': item,
				'expired': item.expire_date <= datetime.date.today(),
			}
		else:
			context = {
				'item': item,
			}
		return context

class CategoryListView(ListView):
	model = Item
	template_name = 'store.html'
	paginate_by = 12

	def get_queryset(self):
		items = Item.objects.filter(category=self.kwargs.get('pk')).order_by('-date_posted')
		return items

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all().order_by('-date_posted')
		return context

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Category
	fields = ['name']
	template_name = 'category_form.html'

	def test_func(self):
		if self.request.user.is_superuser:
			return True
		return False

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class OrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
	model = Order
	template_name = 'orders.html'

	def get_context_data(self, *args, **kwargs):
		order = Order.objects.all()
		context = {
			'orders': order.exclude(status=2).order_by('date_ordered'),
			'fforders': order.filter(status=2).order_by('-date_ordered'),
			'orders_unff': order.filter(status=0).count(),
			'orders_enr': order.filter(status=1).count(),
			'orders_ff': order.filter(status=2).count(),
		}
		return context

	def test_func(self):
		if self.request.user.is_superuser:
			return True
		return False

def purchaseSuccess(request, pk):
	item = Item.objects.get(id=pk)
	messages.success(request, f'Purchase Successful.')
	return redirect('item-detail', item.id)

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			name = request.user.username
			email = request.user.email
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			send_mail(
				"{} ({}): {}".format(name, email, subject),
				message,
				settings.EMAIL_HOST_USER,
				[settings.EMAIL_HOST_USER],
				fail_silently=True,
			)
			messages.success(request, f'Email Sent.')
			return redirect('contact')
	else:
		form = ContactForm()
	return render(request, 'contact.html', {'form': form})

@csrf_exempt
def stripe_config(request):
	if request.method == 'GET':
		stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
		return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request, pk):
	item = Item.objects.get(id=pk)
	if ((item.expire_date is None) or (item.expire_date > datetime.date.today())) and (item.sales_limit == -1 or item.sales_limit - item.sold > 0):
		item.sold += 1
		item.save()
		if request.method == 'GET':
			if settings.DEBUG:
				domain_url = "http://localhost:8000/"
			stripe.api_key = settings.STRIPE_SECRET_KEY
			try:
				checkout_session = stripe.checkout.Session.create(
					success_url=domain_url + "purchase-success/" + str(pk),
					cancel_url=domain_url + "item/" + str(pk),
					payment_method_types=['card'],
					expires_at=int(time.time() + 1800),
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
					],
					shipping_address_collection={
						"allowed_countries": ['US']
					}
				)
				return JsonResponse({'sessionId': checkout_session['id']})
			except Exception as e:
				return JsonResponse({'error': str(e)})
	else:
		return HttpResponse(status=400)

@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']

	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, endpoint_secret
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)

	if event['type'] == 'checkout.session.completed':
		item = Item.objects.get(id=event.data.object.cancel_url.split("item/")[1])
		order = Order(item=item, address=event.data.object.shipping_details.address)
		order.save()
	elif event['type'] == 'checkout.session.expired':
		item = Item.objects.get(id=event.data.object.cancel_url.split("item/")[1])
		item.sold -= 1
		item.save()

	return HttpResponse(status=200)

@csrf_exempt
def status_change(request):
	id = request.POST.get("id")
	order = Order.objects.get(id=id)
	order.status += 1
	order.save()

	return HttpResponse()