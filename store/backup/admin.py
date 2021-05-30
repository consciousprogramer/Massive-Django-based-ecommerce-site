from django.contrib import admin
from .models import *
import admin_thumbnails
import nested_admin
from django.contrib.auth.admin import UserAdmin
# from django_admin_listfilter_dropdown.filters import DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter

# StackedInline
@admin_thumbnails.thumbnail('Image')
class Topbar_imagesInline(admin.TabularInline):
    model = Topbar_images

class TopbarAdmin(admin.ModelAdmin):
    model=TopBar
    inlines = [
        Topbar_imagesInline
    ]
    class Media:
        js = ('store/js/imagePreview.js',)
        css = {
            'all':('store/css/imagePreview.css',)
        }

@admin_thumbnails.thumbnail('Image')
class Slide_pcInline(admin.TabularInline):
    model = Slide_pc
    extra = 1

@admin_thumbnails.thumbnail('Image')
class Slide_mobInline(admin.TabularInline):
    model = Slide_mob
    extra = 1

class SliderAdmin(admin.ModelAdmin):
    model = Slider
    inlines = [
        Slide_pcInline,
        Slide_mobInline
    ]

class Product_imagesInline(admin.TabularInline):
    model = Product_images
    extra = 3

    
class Product_typeAdmin(admin.ModelAdmin):
    search_fields = ['Name']
    ordering = ['Name']
    class Media:
        js = ('store/js/jsonGUI.js',)
        css = {
            'all':('store/css/jsonGUI.css',)
        }

@admin.register(Product)
@admin_thumbnails.thumbnail('Main_image')
class ProductAdmin(admin.ModelAdmin):
    model=Product
    inlines = [
        Product_imagesInline,
    ]
    autocomplete_fields = ['Type','Categorey','Brand']
    filter_horizontal = ('Tags',)
    search_fields = ['Name','id']
    class Media:
        js = ('store/js/jsonGUI.js',)
        css = {
            'all':('store/css/jsonGUI.css',)
        }


@admin.register(Categorey)
@admin_thumbnails.thumbnail('Image')
class CategoreyAdmin(admin.ModelAdmin):
    models = Categorey
    search_fields = ['Name',]
    list_display = ['Name','Show_on_mainpage','Image_thumbnail']
    list_editable = ['Show_on_mainpage',]


@admin.register(SubCategorey)
@admin_thumbnails.thumbnail('Image')
class SubCategoreyAdmin(admin.ModelAdmin):
    model = SubCategorey
    search_fields = ['Name',]
    ordering = ['Name']
    list_display = ['Name','Show_on_mainpage','Image_thumbnail']
    list_editable = ['Show_on_mainpage',]
    filter_horizontal = ('Parent_categorey',)


@admin.register(Brand)
@admin_thumbnails.thumbnail('Brand_image')
class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ('Name','Created','Brand_image_thumbnail')
    search_fields = ['Name',]
# -------------------------------------------------------------------------------------------
@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(nested_admin.NestedModelAdmin):
    model = ProductAttributeValue

class ProductAttributeValueInline(nested_admin.NestedTabularInline):
    model = ProductAttributeValue
    extra = 1
    autocomplete_fields = ['Attribute','Variant']

@admin_thumbnails.thumbnail('Main_image')
class VariantInline(nested_admin.NestedStackedInline):
    model = Variant
    inlines = [ProductAttributeValueInline]
    extra = 0

@admin.register(ProductWithVariant)
@admin_thumbnails.thumbnail('Main_image')
class ProductWithVariantAdmin(nested_admin.NestedModelAdmin):
    model = ProductWithVariant
    inlines = [VariantInline,]
    autocomplete_fields = ['Type','Categorey','Brand']
    filter_horizontal = ('Tags',)
    search_fields = ['Name',]
    list_display = ('id','Name','Is_active','Created','Main_image_thumbnail')
    list_editable = ('Is_active',)
    class Media:
        js = ('store/js/jsonGUI.js',)
        css = {
            'all':('store/css/jsonGUI.css',)
        }

@admin.register(ProductAttribute)
class ProductAttributeAdmin(nested_admin.NestedModelAdmin):
    model = ProductAttribute
    # inlines  = [ProductAttributeValueInline,]
    search_fields = ['Name',]

@admin.register(Variant)
@admin_thumbnails.thumbnail('Main_image')
class VariantAdmin(nested_admin.NestedModelAdmin):
    model = Variant
    search_fields = ['Name','id']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    filter_horizontal = ('Products','Variants')

@admin.register(ProductRow)
class ProductRowAdmin(admin.ModelAdmin):
    model = ProductRow
    filter_horizontal = ('Products','Variants')


class UserAdmin(UserAdmin):
    model = User
    list_display = ['id','__str__']

class CustomerInline(admin.StackedInline):
    model = Customer

@admin.register(User)
class ExtendUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [CustomerInline,]


@admin.register(Customer)
class CustomerAdmin(nested_admin.NestedModelAdmin):
    model = Customer
    
class OrderProductInline(nested_admin.NestedTabularInline):
    model = OrderProduct
    autocomplete_fields = ['Product']

class OrderVariantInline(nested_admin.NestedTabularInline):
    model = OrderVariant
    autocomplete_fields = ['Variant']

@admin.register(Order)
class OrderAdmin(nested_admin.NestedModelAdmin):
    model = Order
    inlines = [
        OrderProductInline,
        OrderVariantInline,
    ]

class CartVariantInline(admin.TabularInline):
    model = CartVariant
    extra = 0

class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [
        CartProductInline,
        CartVariantInline,
    ]


@admin.register(PaymentMethod)
class PaymentMethodAdmin(nested_admin.NestedModelAdmin):
    model = PaymentMethod


@admin.register(OrderProduct)
class OrderProductAdmin(nested_admin.NestedModelAdmin):
    model = OrderProduct


@admin.register(OrderVariant)
class OrderVariantAdmin(nested_admin.NestedModelAdmin):
    model = OrderVariant


@admin.register(CartProduct)
class CartProductAdmin(nested_admin.NestedModelAdmin):
    model = CartProduct


@admin.register(CartVariant)
class CartVariantAdmin(nested_admin.NestedModelAdmin):
    model = CartVariant


@admin.register(ShippingAddress)
class ShippingAddressAdmin(nested_admin.NestedModelAdmin):
    model = ShippingAddress

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    model = Banner


# Register your models here.
admin.site.register(Product_type,Product_typeAdmin)
admin.site.register(TopBar,TopbarAdmin)
admin.site.register(Slider,SliderAdmin)
admin.site.register(Tag)
admin.site.register(Fileshare)
