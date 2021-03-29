from django.db import models
from django.forms import ModelForm, TextInput, EmailInput
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


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
    icon = models.ImageField(upload_to = 'setting_img/icon_image')
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

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.email) + " (" + str(self.confirmed) + ")"
        

class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)  
        for sub in subscribers:
            message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=sub.email,
                    subject=self.subject,
                    html_content=contents + (
                        '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                            request.build_absolute_uri('/delete/'),
                            sub.email,
                            sub.conf_num))
            sg.send(message)









