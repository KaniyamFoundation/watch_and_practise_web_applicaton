from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField

import uuid


class Category(models.Model):
		"""
			This schema holds category names
		"""
		name = models.CharField(max_length=255, blank=False, null=False)
		created_on = models.DateTimeField(auto_now_add=True)
		updated_on = models.DateTimeField(auto_now_add=True)
		
		def __str__(self):
				return self.name


class Tag(models.Model):
		"""
			This schema holds tag names
		"""
		name = models.CharField(max_length=100, null=False, blank=False, unique=True)
		
		def __str__(self):
				return self.name


class Organizer(models.Model):
		"""
			This schema hold author details
		"""
		name = models.CharField(max_length=255, null=False, blank=False)
		profession = models.CharField(max_length=255, null=True, blank=True)
		description = models.TextField(null=True, blank=True)
		social_links = JSONField(null=True)
		city = models.CharField(max_length=155, null=True, blank=True)
		state = models.CharField(max_length=155, null=True, blank=True)
		country = models.CharField(max_length=100, null=True, blank=True)
		is_active = models.BooleanField(default=True)
		is_deleted = models.BooleanField(default=False)
		created_on = models.DateTimeField(auto_now_add=True)
		updated_on = models.DateTimeField(auto_now_add=True)
		
		def __str__(self):
				return self.name
		

class Event(models.Model):
		"""
			This schema holds event related details
		"""
		event_id = models.UUIDField(default=uuid.uuid4, max_length=255, null=False, blank=False, db_index=True)
		title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
		category = models.ForeignKey(Category, null=True, blank=False, on_delete=models.SET_NULL)
		tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
		location = models.CharField(max_length=255, null=True, blank=True)
		city = models.CharField(max_length=255, null=True, blank=True)
		prerequisites = models.TextField(null=True, blank=True)
		organiser = models.ForeignKey(Organizer, null=True, blank=True, on_delete=models.SET_NULL)
		event_date = models.DateTimeField(null=False)
		is_active = models.BooleanField(default=True)
		is_deleted = models.BooleanField(default=False)
		
		created_on = models.DateTimeField(auto_now_add=True)
		updated_on = models.DateTimeField(auto_now_add=True)
		
		def __str__(self):
				return self.title


class StreamEvent(models.Model):
		"""
			This schema takes care of Event streaming related data
		"""
		event = models.ForeignKey(Event, on_delete=models.CASCADE)
		youtube_url = models.URLField(null=True, blank=True)
		etherpad_url = models.URLField(null=True, blank=True)
		created_on = models.DateTimeField(auto_now_add=True)
		updated_on = models.DateTimeField(auto_now_add=True)


