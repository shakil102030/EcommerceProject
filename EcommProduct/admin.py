from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails
from .models import Category, Product, Images, Comment, Color, Size, Variants

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                Product,
                'category',
                'products_count',
                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


@admin_thumbnails.thumbnail('image')
class productImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    #readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_at', 'updated_at']
    list_filter = ['title', 'category', 'created_at']
    list_per_page = 10
    search_fields = ['title', 'new_price', 'detail']
    inlines = [productImageInline, ProductVariantsInline]
    #prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    #readonly_fields = ('subject','comment','ip','user','product','rate','id')
    list_per_page = 10

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'image_id', 'quantity', 'price', 'image_tag']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
