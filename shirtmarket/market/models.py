from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Item(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	image = models.ImageField(default='item_default.jpg', upload_to='item_pics')
	date_posted = models.DateTimeField(default=timezone.now)
	price = models.IntegerField(default=2499)
	sales_limit = models.IntegerField(default=-1, validators=[MinValueValidator(-1)])
	total_rating = models.IntegerField(default=0)
	rating_count = models.IntegerField(default=0)
	sold = models.IntegerField(default=0)

	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse('item-detail', kwargs={'pk': self.pk})

class Favorite(models.Model):
	user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
	item = models.ForeignKey(Item, related_name='favorites', on_delete=models.CASCADE)

class Review(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, related_name='review', on_delete=models.CASCADE)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	def __str__(self):
		return self.title

class Purchased(models.Model):
	user = models.ForeignKey(User, related_name='purchased', on_delete=models.CASCADE)
	item = models.ForeignKey(Item, related_name='purchased', on_delete=models.CASCADE)
