# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Fish(models.Model):
	name = models.CharField(max_length=255)
	created = models.DateTimeField('auto_now_add=True')
	active = models.BooleanField()


class Category(models.Model):
	categoryName = models.CharField(max_length=255)


class Subcategory(models.Model):
	subcategoryName = models.CharField(max_length=255)
	category = models.ForeignKey('Category', on_delete=models.CASCADE)
    

class Partner(models.Model):
	subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, null=True)
	
	deal_id = models.IntegerField()
	title = models.CharField(max_length=500, null=True)
	title_short = models.CharField(max_length=500, null=True)
	price = models.IntegerField(null=True)
	full_price = models.IntegerField(null=True)
	discount = models.IntegerField(null=True)
	economy = models.IntegerField(null=True)
	bought = models.IntegerField(null=True)
	timeout = models.DateTimeField()
	lat = models.FloatField()
	lon = models.FloatField()
	address = models.CharField(max_length=500, null=True)
	schedule = models.CharField(max_length=500, null=True)
	plate_image_exists = models.BooleanField(max_length=500)
	image_url = models.CharField(max_length=500, null=True)

	def __str__(self):
		return "%s" % self.deal_id


class User(models.Model):
	token = models.CharField(max_length=500)
	partners = models.ManyToManyField(Partner)
	categories = models.ManyToManyField(Subcategory, through='Counter')
	categoriesTotal = models.ManyToManyField(Category, through='CounterTotal')

	def __str__(self):
		return self.token

class Counter(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
	counter = models.IntegerField(default=0)

class CounterTotal(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	counter = models.IntegerField(default=0)	









