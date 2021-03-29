from django.contrib import admin
from Blog.models import BlogGrid, Comment
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from EcommerceApp.models import Subscriber
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
import random
import os
from django.http import HttpResponse 

class BlogGridAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content', 'details', 'tags']
    actions = ['mail_posts']

    class Media:
        js = ('tinyinject.js',)
        css = {
             'all': ('tinycss.css',)
        }

    def mail_posts(self, request, queryset):
        datatuple = list()
        
        recipients = Subscriber.objects.all()
        recipients = [recipient.email for recipient in recipients]
        print(recipients)

        for post in queryset:
            subject = post.title
            text = post.details

            extra_posts = BlogGrid.objects.all()
            extra_2_posts = random.choices(extra_posts, k=2)

            content = strip_tags(post.content)

            current_site = Site.objects.get_current()

            html = render_to_string('mail_template.html', {'post': post, 'content': content, 'extra_2_posts': extra_2_posts, 'site': current_site})
            
            complete_info = (subject, text, html, None, recipients)
            datatuple.append(complete_info)


        def send_mass_html_mail(datatuple, fail_silently=True, user=None, password=None, 
                                connection=None):
            connection = connection or get_connection(
                username=user, password=password, fail_silently=fail_silently)
            messages = []
            for subject, text, html, from_email, recipient in datatuple:
                message = EmailMultiAlternatives(subject, text, from_email, recipient)
                message.attach_alternative(html, 'text/html')
                messages.append(message)
            return connection.send_messages(messages)

        print(send_mass_html_mail(datatuple))

        return HttpResponse('mail sent !')

admin.site.register(BlogGrid, BlogGridAdmin)
admin.site.register(Comment)

