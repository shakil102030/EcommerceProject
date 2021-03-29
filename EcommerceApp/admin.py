from django.contrib import admin
from EcommerceApp.models import Setting, ContactMessage, FAQ, Subscriber, Newsletter
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'updated_at', 'status']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'updated_at', 'status']
    #readonly_fields =('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordernumber', 'question', 'status', 'created_at', 'updated_at']
    list_filter = ['status']

def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

send_newsletter.short_description = "Send selected Newsletters to all subscribers"


class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]



admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Subscriber)
admin.site.register(Newsletter, NewsletterAdmin)


