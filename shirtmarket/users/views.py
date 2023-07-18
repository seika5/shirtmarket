from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from market.models import Item
from django.shortcuts import get_object_or_404

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created! You may now log in. ({username})')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form': form})

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