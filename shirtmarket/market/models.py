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
	sold = models.IntegerField(default=0)

	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse('item-detail', kwargs={'pk': self.pk})

class Order(models.Model):
	item = models.ForeignKey(Item, related_name='order', on_delete=models.CASCADE)
	address = models.TextField()
	date_ordered = models.DateTimeField(default=timezone.now)
	status = models.IntegerField(default=0)