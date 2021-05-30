from store.models import ProductWithVariant, Slide_pc, Slide_mob, Slider, User, Variant, Customer,Cart
import os
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=ProductWithVariant)
def assign_thumb_path(sender, instance, **kwargs):
    print('Signal Called')
    allVars = instance.Variants.all()
    for variant in allVars:
        print(f'saving -{variant.id}')
        variant.save()


@receiver(post_save, sender=Slide_pc)
def count_slide_pc(sender, instance, created, **kwargs):
    print('Saved Slide_pc Updating Parent')
    if created:
        instance.Related_slider.SliderCount_pc = instance.Related_slider.SliderCount_pc + 1
        instance.Related_slider.save(update_fields=['SliderCount_pc'])


@receiver(post_save, sender=Slide_mob)
def count_slide_mob(sender, instance, created, **kwargs):
    print('Saved Slide_mob Updating Parent')
    if created:
        instance.Related_slider.SliderCount_mob = instance.Related_slider.SliderCount_mob + 1
        instance.Related_slider.save(update_fields=['SliderCount_mob'])


@receiver(pre_delete, sender=Slider)
def remove_slide_pc(sender, instance, **kwargs):
    allPc = instance.Slides_pc.all()
    allMob = instance.Slides_mob.all()
    instance.On_delete = True
    instance.save(update_fields=['On_delete'])
    for slide in allPc:
        slide.delete()
    for slide in allMob:
        slide.delete()


@receiver(pre_delete, sender=Slide_pc)
def remove_slide_pc(sender, instance, **kwargs):
    if instance.Related_slider.On_delete != True:
        instance.Related_slider.SliderCount_pc = instance.Related_slider.SliderCount_pc - 1
        instance.Related_slider.save()


@receiver(pre_delete, sender=Slide_mob)
def remove_slide_mob(sender, instance, **kwargs):
    if instance.Related_slider.On_delete != True:
        instance.Related_slider.SliderCount_mob = instance.Related_slider.SliderCount_mob - 1
        instance.Related_slider.save()

# ---------------------------------
# @receiver(post_save,sender=Variant)
# def cache_attribute_details(sender,instance,**kwargs):
#     # Working Signal But, Currenttly Not Being Used
#     attrvals = instance.Attributevalue.all().select_related('Attribute').values_list('Attribute__Name','Value')
#     mapping = {
#         'attrList' : [],
#         'attrRead' : []
#     }
#     for attr in attrvals:
#         mapping['attrList'].append({'attrName':attr[0],'value':attr[1]})
#     print(mapping)

# ----------------------------------
# @receiver(post_save,sender=User)
# def create_customer_and_cart(sender,instance,created,**kwargs):
#     if created:
#         if instance.Customer == None:
#             customer = Customer()
#             customer.User = instance


@receiver(post_save,sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(User=instance)
    instance.Customer.save()

@receiver(pre_save, sender=Customer)
def create_cart(sender, instance, **kwargs):
    if not instance.pk:
        instance.Cart = Cart.objects.create()
    instance.Cart.save()

@receiver(post_delete,sender=Customer)
def delete_cart(sender,instance,**kwargs):
    Cart.objects.get(id=instance.Cart_id).delete()
