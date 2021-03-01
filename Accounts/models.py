from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	phone = models.CharField(max_length = 20, blank = True)
	address = models.CharField(max_length = 190, blank = True)
	city = models.CharField(max_length = 190, blank = True)
	country = models.CharField(max_length = 190, blank = True)
	image = models.ImageField(blank = True, upload_to = 'images/users/')

	def __str__(self):
		return self.user.username

	def UserName(self):
		return self.user.first_name+' '+ self.user.last_name+'['+self.user.username+']'
	
	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""

	def ImageTag(self):
		return mark_safe('<img src="{}" heights="50" width="50" />'.format(self.image.url))
	ImageTag.short_description='Image'



	
