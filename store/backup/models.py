from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField,JSONField
from django.core.validators import MaxValueValidator,MinValueValidator,MinLengthValidator
from imagekit.models import ImageSpecField,ProcessedImageField
from imagekit.processors import ResizeToFit #,ResizeToCover,ResizeToFill,SmartResize
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# from django.contrib.postgres.search import SearchQuery,SearchVector



def return_array():
    return []

def return_dict():
    return {}

# not in use currently
def has_changed(instance, field):
    if not instance.pk:
        return False
    old_value = instance.__class__._default_manager.filter(id=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value


GENDER = (("male","MALE"),("female","FEMALE"))
ADDRESSTYPES = (('HOME','HOME') , ('WORK','Work/Office'))
ORDERSTATUS = (
    ('-1','Error'),
    ('0','Placed'),
    ('1','Order Recived'),
    ('2','Declined By Seller'),
    ('3','Cancelation Requested'),
    ('4','Cancel Completed'),
    ('5','Packed & Bill Genrated'),
    ('6','Shipped Out'),
    ('7','On The Way'),
    ('8','Completed'),
    ('9','Declined By Buyer'),
    ('10','Return Requested'),
    ('11','Return Completed'),
    ('12','Disputed'),
    ('13','Verification Required'),
    )


class User(AbstractUser):
    pass
    def __str__(self):
        return self.first_name.capitalize() + " " + self.last_name.capitalize()
    



class Customer(models.Model):
    User = models.OneToOneField('User',related_name='Customer',on_delete=models.CASCADE,blank=True,default=None,null=True)
    Cart = models.OneToOneField('Cart',on_delete=models.CASCADE,related_name='Customer',blank=True,default=None,null=True)
    Joined = models.DateTimeField(default=timezone.now,blank=True,editable=False)
    Email = models.EmailField(unique=True,blank=True,default=None,null=True)
    PhoneNumber = models.CharField(max_length=10,help_text='10 Digit Phonenumber')
    TotalPurchase = models.PositiveIntegerField(default=0,blank=True)
    NumberOfOrders = models.PositiveSmallIntegerField(default=0,editable=False,blank=True)
    ShoppedCategories = JSONField(default=return_dict,blank=True)
    ShoppedSubCategories = JSONField(default=return_dict,blank=True)
    # ProfilePic = models.ImageField(upload_to='profiles/profilepics',default='./store/images/avatar/avt.png',blank=True)
    # Gender = models.CharField(choices = GENDER,default = "male",blank = True,max_length = 6)
    # reverse from ShippingAddress (done)
    # reverse from orders 
    # reverse from Questions
    
    def __str__ (self):
        return self.User.first_name.capitalize()+ " " + str(self.pk) + " " + self.User.last_name.capitalize()

    def save(self,*args,**kwargs):
        super(Customer,self).save(*args,**kwargs)

class Order(models.Model):
    Customer = models.ForeignKey('Customer',related_name='Orders',on_delete=models.SET_NULL,null=True,editable=False)
    ShippingAddress = models.ForeignKey('ShippingAddress',related_name='Orders',on_delete=models.PROTECT,editable=False)
    OrderDate = models.DateTimeField(auto_now_add=True,blank=True,editable=False)
    LastModified = models.DateTimeField(default=timezone.now)
    Status = models.CharField(choices=ORDERSTATUS,default='0',max_length=64)
    TotalPrice = models.PositiveIntegerField(editable=False)
    Method = models.ForeignKey('PaymentMethod',related_name='Orders',editable=False,on_delete=models.SET_NULL,null=True)
    # Meta Details
    Categories = models.ManyToManyField('Categorey',related_name='In_orders',editable=False,blank=True)
    SubCategories = models.ManyToManyField('SubCategorey',related_name='In_orders',editable=False,blank=True)
    SellerComments = models.TextField(default='No Comments From Seller!')
    DaysForCompletion = models.PositiveSmallIntegerField(default=None,null=True,blank=True,editable=False)
    FeedbackRating = models.PositiveSmallIntegerField(default=None,null=True,blank=True,editable=False)
    FeedbackComment = models.TextField(max_length=600,default=None,null=True,blank=True,editable=False)

    def __str__(self):
        return f'ID: {self.pk} of-{self.Customer.User.first_name}'

class PaymentMethod(models.Model):
    Name = models.CharField(unique=True,max_length=64)
    CodeWord = models.CharField(unique=True,max_length=64)
    Is_active = models.BooleanField(default=True)
    Created = models.DateTimeField(default=timezone.now,blank=True,editable=False)
    
    def save(self,*args,**kwargs):
        self.CodeWord = self.CodeWord.lower()
        self.Name = self.Name.capitalize()
        super(PaymentMethod,self).save(*args,**kwargs)
    
    def __str__(self):
        return f'{self.Name}'
# ------------------- ORDER ITEMS ----------------------
class OrderProduct(models.Model):
    Product = models.ForeignKey('Product',on_delete=models.PROTECT,related_name='In_orders')
    Order = models.ForeignKey(Order,related_name='Orderprod',on_delete=models.CASCADE)
    Quantity = models.PositiveSmallIntegerField()
    Added = models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return f'{self.Product.Name[0:20]}... | Nos :{self.Quantity}'

class OrderVariant(models.Model):
    Variant = models.ForeignKey('Variant',on_delete=models.PROTECT,related_name='In_orders')
    Order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='Ordervar')
    Quantity = models.PositiveSmallIntegerField()
    Added = models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return f'{self.Variant.Name[:20]}... | Nos :{self.Quantity}'
# ------------------- ORDER ITEMS ----------------------

# ------------------- CART ITEMS ----------------------

class CartProduct(models.Model):
    Product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='In_carts')
    Quantity = models.PositiveSmallIntegerField()
    Added = models.DateTimeField(auto_now_add=True)
    Cart = models.ForeignKey('Cart',related_name='Cartproduct',on_delete=models.CASCADE)
    ForLater = models.BooleanField(default=False)

    def __str__ (self):
        return f'id: {self.id} {self.Product.Name[0:20]} ... | Nos :{self.Quantity}'    


class CartVariant(models.Model):
    Variant = models.ForeignKey('Variant',on_delete=models.CASCADE,related_name='In_carts')
    Quantity = models.PositiveSmallIntegerField()
    Added = models.DateTimeField(auto_now_add=True)
    Cart = models.ForeignKey('Cart',related_name='Cartvariant',on_delete=models.CASCADE)
    ForLater = models.BooleanField(default=False)

    def __str__ (self):
        return f'id: {self.id} {self.Variant.Name[:20]}... | Nos :{self.Quantity}'

# ------------------- CART ITEMS ----------------------

# CART Model
class Cart(models.Model):
    # Product = models.ManyToManyField(CartProduct,related_name='Carts')
    # Variant = models.ManyToManyField(CartVariant,related_name='Carts')
    LastModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            a = f'{self.pk} Cart of {self.Customer.User.first_name.capitalize()}'
        except:
            a = 'Error in showing name!'
        return a
    

class ShippingAddress(models.Model):
    Owner = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='ShippingAddressOptions')
    Father = models.CharField(max_length=164,verbose_name='(C/O) Gaurdian Name',blank=True,default='Not Applicable')
    OwnerName = models.CharField(max_length=256,verbose_name='Name')
    PhoneNumber = models.BigIntegerField(verbose_name='Main Phone Number',validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)],help_text='Your Main Phone Number')
    AltPhoneNumber = models.BigIntegerField(verbose_name='Alternate [ Second ] Phone Number',validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)],help_text='If First Phone Number Will Not Work, We Will Use This')
    City = models.CharField(max_length=128,verbose_name='City/Town/Village')
    District = models.CharField(max_length=128,verbose_name='District Name')
    PIN = models.PositiveIntegerField(verbose_name='PIN Code')
    State = models.CharField(max_length=128)
    LandMark = models.CharField(max_length=164,help_text='(Optional)\nEx-opposite SBI or near this building...')
    Address = models.TextField(max_length=720,help_text='Area Name and Gali/Street Number')
    AddressType = models.CharField(max_length=164,choices=ADDRESSTYPES,default='HOME',help_text=f'HOME : For All Day Delivery <br> OFFICE : For Delivery Between 9AM - 6PM')

    def __str__(self):
        return f'id: {self.pk} owner:{self.OwnerName} ,for:{self.Owner.User.first_name}'
    


# Create your models here
class TopBar(models.Model):
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Name = models.CharField(max_length=256,verbose_name='Topbar Name',help_text='Example - Newyear Topbar, New Session Topbar')
    Active = models.BooleanField(default=False,verbose_name='Show on Main Page')
    def __str__(self):
        return self.Name

# not To Register
class Topbar_images(models.Model):
    Name = models.CharField(max_length=48,verbose_name='Categorey Name',help_text='Example - Markers, GK Books, Pencil Colors')
    # Image = models.ImageField(upload_to="genimages",verbose_name='Categorey Image')
    Image = ProcessedImageField(upload_to='genimages',
                                           processors=[ResizeToFit(110, 110)],
                                           format='JPEG',
                                           options={'quality': 80})
    Related_topbar = models.ForeignKey('Topbar',related_name='Images',on_delete=models.CASCADE)
    GotoUrl = models.URLField()
    def __str__(self):
        return self.Name
    
class Brand(models.Model):
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Name = models.CharField(max_length=64,verbose_name='Brand Name')
    Brand_image = ProcessedImageField(upload_to='brand/images',
                                           processors=[ResizeToFit(120,120)],
                                           format='JPEG',
                                           options={'quality': 90})
    def __str__(self):
        return self.Name

class Tag(models.Model):
    Name = models.CharField(max_length = 64)
    Created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Name

class Slider(models.Model):
    Name = models.CharField(max_length=128)
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=False,verbose_name='Show on Main Page')
    SliderCount_pc = models.PositiveSmallIntegerField(editable=False,blank=True,default=0)
    SliderCount_mob = models.PositiveSmallIntegerField(editable=False,blank=True,default=0)
    On_delete = models.BooleanField(editable=False,blank=True,default=False)
    
    def __str__(self):
        return self.Name
    
    class Meta:
        verbose_name = 'Main Slider'
    
    def save(self,*args, **kwargs):
        super(Slider,self).save(*args, **kwargs)
        print(f'PC -{self.Slide_pc.all().count()}')
        print(f'MOB -{self.Slide_mob.all().count()}')
        # self.SliderCount_pc = self.Slide_pc.all().count()
        # self.SliderCount_mob = self.Slide_mob.all().count()

# Not To register
class Slide_pc(models.Model):
    Image = models.ImageField(upload_to='slider/pc_images')
    Related_slider = models.ForeignKey(Slider,related_name='Slide_pc',on_delete=models.CASCADE)
    GotoLink = models.URLField(max_length=200,verbose_name='Linked URL/Page',blank=True,default='')

class Slide_mob(models.Model):
    Image = models.ImageField(upload_to='slider/mob_images')
    Related_slider = models.ForeignKey(Slider,related_name='Slide_mob',on_delete=models.CASCADE)
    GotoLink = models.URLField(max_length=200,verbose_name='Linked URL/Page',blank=True,default='')
    # Variant = models.ForeignKey("Variant",related_name='Slide_mob',on_delete=models.CASCADE,null=True,default=None,blank=True)

# ALIAS ->  Categorey Group
class Categorey(models.Model):
    Image = ProcessedImageField(upload_to='Categorey/images',
                                           processors=[ResizeToFit(120,120)],
                                           format='JPEG',
                                           options={'quality': 80})
    Show_on_mainpage = models.BooleanField(default=False)
    Name = models.CharField(max_length=64,verbose_name='Categorey Group Name',help_text='Example - Schools, Classwise, Office, Pen and Pencils')
    Created = models.DateTimeField(auto_now_add=True)
    # Add Image field for Every Categorey for Visual Cue
    class Meta:
        verbose_name = _("Categorey")
        verbose_name_plural = _("Categorey")
    def __str__(self):
        return self.Name
     
# ALIAS ->  Categorey
class SubCategorey(models.Model):
    Image = ProcessedImageField(upload_to='SubCategorey/images',
                                           processors=[ResizeToFit(120,120)],
                                           format='JPEG',
                                           options={'quality': 80})
    Show_on_mainpage = models.BooleanField(default=False)
    Name = models.CharField(max_length=64,verbose_name='Categorey Name')
    Parent_categorey = models.ManyToManyField(Categorey,verbose_name='In Categorey Group',related_name='Subcategorey')
    class Meta:
        verbose_name = _("Sub-Categorey")
        verbose_name_plural = _("Sub-Categories")

    def __str__(self):
        return f'{self.Name}'

class Product_type(models.Model):
    Name = models.CharField(max_length=200,verbose_name='Type')
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Meta_data = ArrayField(models.CharField(max_length=150),default=return_array,verbose_name='Details')
    # Product_type_attributes = models.ManyToManyField("ProductAttribute",related_name='Product_types')
    class Meta:
        verbose_name = _("Product_type")
        verbose_name_plural = _("Product_types")
    def __str__(self):
        return self.Name

# Not To Register
class Product_images(models.Model):
    Title = models.CharField(max_length=164)
    Main_image = models.ImageField(upload_to='products/images/highres',help_text='This will be the high quality image')
    Thumbnail = ImageSpecField(source = 'Main_image',
                            processors=[ResizeToFit(500,500)],
                            format='JPEG',
                            options={'quality': 80},
                            )
    Related_product = models.ForeignKey('Product',related_name='Its_images',on_delete=models.CASCADE,default=1)
    Thumb_path = models.CharField(max_length=364,blank=True,editable=False)

    def save(self,*args, **kwargs):
        self.Thumb_path = self.Thumbnail.url
        super(Product_images,self).save(*args, **kwargs)
    # def save(self,*args, **kwargs):
    #     if has_changed(self,'Images'):
    #         print('-----------CHANGED-----------------')
    #         self.thumb.save(f'{self.Images.name}_thumbnail',self.Images,save=False) 
    #     else:
    #         print('--------------NOT CHANGED-----------')
    #     super(Product_images,self).save(*args, **kwargs)


    # Add Custom Delete

class Product(models.Model):
    # Product Timeline Details
    Is_variant = models.BooleanField(default=False,editable=False,blank=True)
    Is_normal_product = models.BooleanField(default=True,editable=False,blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Added_by = models.CharField(default='Rohit admin',max_length=64,blank=True,editable=False)
    # Important Details
    Name = models.CharField(max_length=512)
    Brand = models.ForeignKey(Brand,related_name='Brans_products',on_delete=models.PROTECT)
    Description = models.TextField()
    Thumbnail = ImageSpecField(source='Main_image',
                                processors=[ResizeToFit(500, 500)],
                                format='JPEG',
                                options={'quality': 90},
                                )
    Thumb_path = models.CharField(max_length=364,blank=True,editable=False)
    Main_image = models.ImageField(upload_to='products/main_images')
    Highlights = ArrayField(models.CharField(max_length=164),default=return_array)
    Type = models.ForeignKey(Product_type,related_name='All_products',on_delete=models.PROTECT)
    Meta_data = JSONField(default=return_dict)
    Cost_to_customer = models.PositiveIntegerField(help_text='Price that customer will PAY!')
    Cost_to_seller = models.PositiveIntegerField(help_text='Total Cost of product for seller')
    Crossed_price = models.PositiveIntegerField(help_text='Price that will be crossed')
    Local_offer = models.PositiveIntegerField(validators=[MaxValueValidator(90)],blank=True,default=0,help_text='Discount percentage (%)')
    Is_active = models.BooleanField(default=True)
    Total_stock = models.PositiveIntegerField()
    Categorey = models.ManyToManyField(SubCategorey,related_name='All_products')
    Tags = models.ManyToManyField(Tag,related_name = 'All_taged_products')
    #Calculation Details
    Rating = models.FloatField(validators=[MaxValueValidator(5),MinValueValidator(0)],editable=False,default=0)
    Nums_of_rating = models.PositiveIntegerField(default=0,blank=True,editable=False)
    Total_sales = models.PositiveIntegerField(default=0,blank=True,editable=False)
    Total_views = models.PositiveIntegerField(default=0,blank=True,editable=False)
    Total_carts = models.PositiveIntegerField(default=0,blank=True,editable=False)
    Sales_probablity = models.FloatField(validators=[MaxValueValidator(1)],default=1,blank=True,editable=False)
    Cart_probablity = models.FloatField(validators=[MaxValueValidator(1),MinValueValidator(0)],default=1,blank=True,editable=False)
    # Remaining_stock = models.PositiveIntegerField(blank=True,editable=False,default=0)
    Discount = models.PositiveSmallIntegerField(blank=True,editable=False)
    def __str__(self):
        return self.Name
    
    def save(self,*args, **kwargs):
        self.Thumb_path = self.Thumbnail.url
        # calculate Discount Percentage
        self.Discount = round(((self.Crossed_price - self.Cost_to_customer)/self.Crossed_price)*100)
        print(self.Discount)
        super(Product,self).save(*args, **kwargs)
            

    # def save(self,*args, **kwargs):
    #     if not self.pk:
    #         old_value = None
    #     else:
    #         old_value = self.objects.filter(id=self.pk).values(field).get()[field]
    #     super(Product,self).save(*args, **kwargs)
    #     if old_value == None:
    #         img = Image.open(self.Main_image)
    #         processor = ResizeToFit(500,500)
    #         self.Thumbnail.save(f'{self.Main_image_thumbnail}.jpg',processor.process(img),save())

class ProductRow(models.Model):
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Name = models.CharField(max_length=128,verbose_name='Tittle')
    ImageText = models.CharField(max_length=128,editable=False,default='')
    Description = models.TextField(max_length=256)
    Poster = models.ImageField(upload_to='Product_row/posters',blank=True)
    Products = models.ManyToManyField(Product,related_name='In_row',blank=True)
    Variants = models.ManyToManyField('Variant',related_name='In_row',blank=True)
    Show_on_mainpage = models.BooleanField(default=False)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'Product Slider'

class Collection(models.Model):
    Name = models.CharField(max_length=128,verbose_name='Tittle')
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Products = models.ManyToManyField(Product,related_name='In_collection',blank=True)
    Variants = models.ManyToManyField('Variant',related_name='In_collection',blank=True)
    # All_variants = models.ManyToManyField('Variant',related_name='In_collection')
    # Will have add varinat product and product varints
    Description = models.TextField(max_length=256)
    Show_on_mainpage = models.BooleanField(default=False)

    def __str__(self):
        return self.Name
    
    class Meta:
        verbose_name = "Package and Bundle"
        verbose_name_plural = "Packages and Bundles"
       
class ProductAttribute(models.Model):
    # EX - Color
    Name = models.CharField(max_length=50)
    # Variants = models.ForeignKey("Variant",related_name='Variants',on_delete=models.CASCADE)
    def __str__(self):
        return f'Attribute: {self.Name}'

    def save(self,*args, **kwargs):
        self.Name = self.Name.lower()
        super(ProductAttribute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Product Feature Name")
        verbose_name_plural = _("Product Feature Name")

# Not to register in admin
class ProductAttributeValue(models.Model):
    Value = models.CharField(max_length=50)
    # Many Values of Color
    Attribute = models.ForeignKey(ProductAttribute,related_name='Attributevalue',on_delete=models.CASCADE)
    Variant = models.ForeignKey('Variant',related_name='Attributevalue',on_delete=models.CASCADE,null=True)
    # AttributeM2m = models.ManyToManyField(ProductAttribute,related_name='M2MAttributevalue')

    class Meta:
        verbose_name = _("Product Feature Value")
        verbose_name_plural = _("Product Feature Value")

    def save(self,*args, **kwargs):
        self.Value = self.Value.lower()
        super(ProductAttributeValue, self).save(*args, **kwargs)

    def __str__(self):
        # Attribute_for_type = self.Attribute.Product_types.all()
        # for_str = ''
        # for attr in Attribute_for_type:
        #     for_str += f'for {attr.Name} '
        # return f'{self.Attribute.Name}-{self.Value} (for-{self.Attribute.For_product_types.Name})'
        # return f'{self.Attribute.Name} = {self.Value} <-------------------------------------------------------------------------------[{for_str}]'
        return f'{self.Attribute.Name} = {self.Value}'

# class ProductAttributeValueOptions(models.Model):
#     Attribute = models.ForeignKey(ProductAttribute,related_name='Attributevalue_group',on_delete=models.PROTECT)
#     Attribute_values

class ProductWithVariant(models.Model):
    Is_variant = models.BooleanField(default=False,editable=False,blank=True)
    Is_normal_product = models.BooleanField(default=False,editable=False,blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Name = models.CharField(max_length=526)
    Name_list = models.CharField(max_length=1024,blank=True,editable=False)
    Brand = models.ForeignKey("store.Brand",on_delete=models.PROTECT)
    Description = models.TextField()
    Thumbnail = ImageSpecField(source='Main_image',
                                processors=[ResizeToFit(500, 500)],
                                format='JPEG',
                                options={'quality': 90},
                                )
    Main_image = models.ImageField(upload_to='varianceproduct/mainimages')
    Thumb_path = models.CharField(max_length=364,blank=True,editable=False)
    Type = models.ForeignKey(Product_type,related_name='All_products_with_variant',on_delete=models.PROTECT)
    Highlights = ArrayField(models.CharField(max_length=164),default=return_array)
    Meta_data = JSONField(default=return_dict)
    Categorey = models.ManyToManyField(SubCategorey,related_name='All_products_with_variant')
    Tags = models.ManyToManyField(Tag,related_name = 'All_products_with_variant')
    Rating = models.FloatField(validators=[MaxValueValidator(5),MinValueValidator(0)],editable=False,default=0)
    Nums_of_rating = models.PositiveIntegerField(default=0,blank=True,editable=False)
    Is_active = models.BooleanField(default=True,verbose_name='Product Status')
    def __str__(self):
        return f'{self.Name}'

    def save(self,*args, **kwargs):
        print(f'-------[In ProductWithVariant]-----{self.Thumbnail.url}----------')
        self.Thumb_path = self.Thumbnail.url
        super(ProductWithVariant,self).save(*args, **kwargs)

class Variant(models.Model):
    # Actually this product will be "Product with Variant"
    Is_variant = models.BooleanField(default=True,editable=False,blank=True)
    Is_normal_product = models.BooleanField(default=False,editable=False,blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Last_updated = models.DateTimeField(auto_now=True)
    Name = models.CharField(max_length=256)
    Thumbnail = ImageSpecField(source='Main_image',
                                processors=[ResizeToFit(500, 500)],
                                format='JPEG',
                                options={'quality': 90},
                                )
    Description = models.TextField(default='',editable=False)
    Highlights = ArrayField(models.CharField(max_length=164),default=return_array,blank=True,editable=False)
    Main_image = models.ImageField(upload_to='variants/images',blank=True)
    Thumb_path = models.CharField(max_length=364,blank=True,editable=False)
    Cost_to_customer = models.PositiveIntegerField(help_text='Price that customer will PAY!')
    Cost_to_seller = models.PositiveIntegerField(help_text='Total Cost of product for seller')
    Crossed_price = models.PositiveIntegerField(help_text='Price that will be crossed')
    Local_offer = models.PositiveIntegerField(validators=[MaxValueValidator(90)],blank=True,default=0,help_text='Discount percentage (%)',verbose_name='Discount in ( % )')
    Is_active = models.BooleanField(default=True,verbose_name='Product Status')
    Total_stock = models.PositiveIntegerField()
    Product = models.ForeignKey("ProductWithVariant", on_delete=models.PROTECT, related_name='Variants')
    AttrCache = JSONField(default=return_dict,blank=True)
    Discount = models.PositiveSmallIntegerField(blank=True,editable=False)
    # AttributeValue = models.ManyToManyField("ProductAttribute",related_name='Variants')
    def __str__(self):
        return f'id:{self.pk} variant of {self.Product.Name}'
    
    def save(self,*args, **kwargs,):
        # calculate Discount Percentage
        self.Discount = round(((self.Crossed_price - self.Cost_to_customer)/self.Crossed_price)*100)
        print(self.Discount)
        # Settele the matter of attribute
        attrvals = self.Attributevalue.all().select_related('Attribute').values_list('Attribute__Name','Value')
        mapping = {
            'attrList' : [],
            'attrRead' : []
        }
        for attr in attrvals:
            mapping['attrList'].append({'attrName':attr[0],'value':attr[1]})
            mapping['attrRead'].append(f'{attr[0]}: {attr[1]}')
        self.AttrCache = mapping
        self.Thumb_path = self.Thumbnail.url
        self.Highlights = self.Product.Highlights
        self.Description = self.Product.Description
        super(Variant,self).save(*args, **kwargs)
    
class VariantImages(models.Model):
    Created = models.DateTimeField(auto_now_add=True)
    Name = models.CharField(max_length=50)
    Main_image = models.ImageField(upload_to='product/images/varinat')
    Variant = models.ForeignKey("Variant", on_delete=models.CASCADE,related_name='Images')
    Thumbnail = ImageSpecField(source='Main_image',
                                processors=[ResizeToFit(500, 500)],
                                format='JPEG',
                                options={'quality': 90},
                                )
    Thumb_path = models.CharField(max_length=364,blank=True,editable=False)
    
    def save(self,*args, **kwargs):
        super(VariantImages,self).save(*args, **kwargs) 
        self.Thumb_path = self.Thumbnail.url
        self.Thumb_path.save()

class Fileshare(models.Model):
    Text = models.TextField(default='',blank=True,null=True)
    ImageFile = models.ImageField(upload_to='fileshare',blank=True,null=True,default=None)
    File = models.FileField(upload_to='fileshare/files',blank=True,null=True,default=None)
    URL = models.URLField(blank=True,null=True,default=None)
    def __str__(self):
        return f'{self.Text[:60].capitalize()}'

BANNER_TYPES = (
    ('0','left'),
    ('1','center'),
    ('2','right'),
    )    
class Banner(models.Model):
    Created = models.DateTimeField(auto_now_add=True)
    Name = models.CharField(max_length=64)
    Description = models.TextField(max_length=164)
    Link = models.URLField()
    BackgroundImage = models.ImageField(upload_to='banner')
    Active = models.BooleanField(default=False)
    Type = models.CharField(choices=BANNER_TYPES,default='normal',max_length=64)
    
    def __str__(self):
        return self.Name
    

