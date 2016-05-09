import uuid
import os
import re
from django.db import models
from tinymce.models import HTMLField
from taggit.managers import TaggableManager

REGISTER_TRANSFER = (
	('E', 'Email'),
	('P', 'Phone'),
	('M', 'Mail'),
	('F', 'Fax'),
	('S', 'SMS'),
	('L', 'Line'),
	('D', 'Direct'),
)

REGISTER_STATUS = (
	('R', 'Register'),
	('P', 'Paid'),
	('T', 'Partial'),
	('C', 'Cancel'),
)

COURSE_LEVEL = (
	('B', 'Basic'),
	('M', 'Medium'),
	('A', 'Advance'),
)

def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = '%s.%s' % (uuid.uuid4(), ext)
	return os.path.join('upload', filename)


def simple_slug(s):
	return re.sub('[!@#$%^&*+/:=()]+', '', s).replace(' ', '-').replace('\\', '').lower()


class Bank(models.Model):
	code = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=100)
	branch = models.CharField(max_length=100, null=True, blank=True)
	image = models.FileField(upload_to=get_file_path, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Bank'

	def __unicode__(self):
		return self.name


class Account(models.Model):
	code = models.CharField(max_length=40, unique=True)
	name = models.CharField(max_length=50)
	bank = models.ForeignKey(Bank, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Account'

	def __unicode__(self):
		return self.name


class Location(models.Model):
	code = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=150)
	lat = models.FloatField(default=0)
	lng = models.FloatField(default=0)
	email = models.EmailField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=50, null=True, blank=True)
	website = models.URLField(max_length=150, null=True, blank=True)
	address = models.TextField(null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Location'

	def __unicode__(self):
		return self.name


class Author(models.Model):
	code = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=100)
	short = models.CharField(max_length=30, null=True, blank=True)
	position = models.CharField(max_length=150, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=50, null=True, blank=True)
	address = models.TextField(null=True, blank=True)
	image = models.FileField(upload_to=get_file_path, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Author'

	def __unicode__(self):
		return self.name


class Category(models.Model):
	code = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=150, null=True, blank=True)
	icon = models.CharField(max_length=30, null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Category'

	def __unicode__(self):
		return self.name


class Course(models.Model):
	code = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=200)
	slug = models.CharField(max_length=200)
	description = HTMLField(null=True, blank=True)
	category = models.ForeignKey(Category)
	authors = models.ManyToManyField(Author)
	accounts = models.ManyToManyField(Account, blank=True)
	price = models.FloatField(default=0)
	hours = models.IntegerField(default=0)
	lessons = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	rating = models.FloatField(default=0)
	level = models.CharField(max_length=1, default='B', choices=COURSE_LEVEL)
	tags = TaggableManager()
	is_hot = models.BooleanField(default=False)
	is_publish = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	image = models.FileField(upload_to=get_file_path, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Course'

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if self.name:
			self.slug = simple_slug(self.name)
		return super(Course, self).save(*args, **kwargs)

	def is_training(self):
		return self.training_set.filter(is_publish=True, is_complete=False).count() > 0


class Training(models.Model):
	name = models.CharField(max_length=200)
	course = models.ForeignKey(Course)
	start = models.DateField(null=True, blank=True)
	finish = models.DateField(null=True, blank=True)
	open_date = models.CharField(max_length=50, null=True, blank=True)
	total_hour = models.IntegerField(default=0)
	time = models.CharField(max_length=30, null=True, blank=True)
	min_people = models.IntegerField(default=0)
	max_people = models.IntegerField(default=0)
	location = models.ForeignKey(Location, null=True, blank=True)
	promotion = models.CharField(max_length=100, null=True, blank=True)
	discount = models.FloatField(default=0)
	unit_price = models.FloatField(default=0)
	sale_price = models.FloatField(default=0)
	is_publish = models.BooleanField(default=False)
	is_complete = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Training'

	def __unicode__(self):
		return self.name


class Member(models.Model):
	name = models.CharField(max_length=150)
	email = models.EmailField(max_length=150, unique=True)
	phone = models.CharField(max_length=30)
	org = models.CharField(max_length=200, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = 'Member'

	def __unicode__(self):
		return self.name


class Register(models.Model):
	trainging = models.ForeignKey(Training)
	member = models.ForeignKey(Member)
	transfer_via = models.CharField(max_length=1, choices=REGISTER_TRANSFER)
	transfer_date = models.DateField(null=True, blank=True)
	transfer_amount = models.FloatField(default=0)
	reg_date = models.DateTimeField(auto_now_add=True)
	reg_status = models.CharField(max_length=1, default='R', choices=REGISTER_STATUS)

	class Meta:
		verbose_name_plural = 'Register'

	def __unicode__(self):
		return '%s %s' % (self.trainging.name, self.member.name)


class Booking(models.Model):
	course = models.ForeignKey(Course)
	member = models.ForeignKey(Member)
	book_date = models.DateTimeField(auto_now_add=True)
	train_date = models.DateField(null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Booking'

	def __unicode__(self):
		return '%s %s' % (self.course.name, self.member.name)
