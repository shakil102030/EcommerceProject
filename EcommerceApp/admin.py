from django.contrib import admin
from EcommerceApp.models import Setting, ContactMessage, FAQ
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'updated_at', 'status']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'updated_at', 'status']
    #readonly_fields =('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordernumber', 'question', 'status', 'created_at', 'updated_at']
    list_filter = ['status']



admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)


