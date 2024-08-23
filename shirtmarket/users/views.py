from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.shortcuts import get_object_or_404
from market.models import Item

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			activateEmail(request, user, form.cleaned_data.get('email'))
			return redirect('market-home')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form': form})

def activateEmail(request, user, email):
	mail_subject = 'Activate your user account.'
	message = render_to_string('activate_account.html', {
		'user': user.username,
		'domain': get_current_site(request).domain,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': account_activation_token.make_token(user),
		'protocol': 'https' if request.is_secure() else 'http'
	})
	email = EmailMessage(mail_subject, message, to=[email])
	if email.send():
		messages.success(request, f'Dear {user}, please go to your email ({email}) and click on \
		    the activation link to confirm and complete the registration. The link expires in 1 hour.')
	else:
		messages.error(request, f'Problem sending confirmation email to {email}, please check if you typed it correctly.')

def activate(request, uidb64, token):
	User = get_user_model()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()

		messages.success(request, 'Success, you can log into your account!')
		return redirect('login')
	else:
		messages.error(request, 'Activation link is invalid!')

	return redirect('landing')

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Account updated.')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)		

	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'profile.html', context)

@login_required
def favorite(request, pk):
	item = get_object_or_404(Item, id=pk)
	if item.favorites.filter(id=request.user.id).exists():
		item.favorites.remove(request.user)
	else:
		item.favorites.add(request.user)
	return HttpResponseRedirect('/item/' + str(pk))

class FavoriteListView(LoginRequiredMixin, ListView):
	model = Item
	template_name = 'favorites.html'

	def get_context_data(self, *args, **kwargs):
		favs = Item.objects.all()
		orders = {
			'favs': favs.filter(favorites=self.request.user).order_by('-date_posted'),
		}
		return orders