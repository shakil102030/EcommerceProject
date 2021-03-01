from django.db import models
from django.forms import ModelForm, TextInput, EmailInput

class Setting(models.Model):

    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length = 200)
    keywords = models.CharField(max_length = 255)
    description = models.TextField(blank = True)
    company = models.CharField(max_length = 50)
    address = models.CharField(blank = True, max_length = 100)
    phone = models.IntegerField()
    fax = models.CharField(blank = True, max_length = 50)
    email = models.EmailField(blank = True, null = True, max_length = 50)
    smtpserver = models.CharField(max_length = 100)
    smtpemail = models.EmailField(blank = True, null = True, max_length = 50)
    smtpassword = models.CharField(blank = True, max_length = 50)
    smtpport = models.CharField(blank = True, max_length = 100)
    icon = models.ImageField(blank = True, null = True, upload_to = 'images/')
    facebook = models.URLField(blank = True, max_length = 100)
    instagram = models.URLField(blank = True, max_length = 100)
    twitter = models.URLField(blank = True, max_length = 100)
    youtube = models.URLField(blank = True, max_length = 100)
    aboutus = models.TextField(blank = True)
    contact = models.TextField(blank = True)
    reference = models.TextField(blank = True)
    status = models.CharField(max_length = 55, choices = STATUS)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title



class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )

    name = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 40)
    subject = models.CharField(blank = True, max_length = 200)
    message = models.TextField(blank = True, max_length = 1000)
    ip = models.CharField(blank = True, max_length = 100)
    Note = models.CharField(blank = True, max_length = 200)
    status = models.CharField(max_length = 40, choices = STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Write your email'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Wrte your Subjects'}),
            'message': TextInput(attrs={'class': 'input', 'placeholder': 'Write your messages','rows':'5'}),
        }

class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length = 200)
    answer = models.TextField(blank = True)
    status = models.CharField(max_length = 200, default = False, choices = STATUS)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.question









