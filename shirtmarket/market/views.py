from django.shortcuts import render
<<<<<<< HEAD

posts = [
	{
		'author': 'ricin',
		'title': 'Market Post 1',
		'content': 'Market Post 1 Content',
		'date_posted': 'April 25, 2023'
	},
	{
		'author': 'hurtburt',
		'title': 'Market Post 2',
		'content': 'Market Post 2 Content',
		'date_posted': 'April 26, 2023'
	}
]

def home(request):
	context = {
		'posts': posts
	}
	return render(request, 'home.html', context)

def about(request):
	return render(request, 'about.html')
=======
from django.http import HttpResponse

def home(request):
	return HttpResponse('<h1>Blog Home</h1>')

def about(request):	
	return HttpResponse('<h1>Blog About</h1>')
>>>>>>> parent of 2eba030 (Revert "initial commit")
