from django.shortcuts import render

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