from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
from . models import *
from django.template.loader import render_to_string
from json import loads,dumps
from django.core.paginator import Paginator
from django.db.models import F,Value,Q
from .forms import ShippingAddressForm,RegisterForm,LoginForm,CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    render_context = {}
    topbar = TopBar.objects.filter(Active=True).prefetch_related('Images').first()
    topbar_html = render_to_string('store/components/Topbar/topbar.html',{'topbar_images':topbar.Images.all()})
    slider = Slider.objects.filter(Active=True).prefetch_related('Slide_pc','Slide_mob').first()
    slider_html = render_to_string('store/components/slider/slider.html',{'slides_pc':slider.Slide_pc.all(),'slides_mob':slider.Slide_mob.all(),'sliderCount_pc':range(0,slider.SliderCount_pc),'sliderCount_mob':range(0,slider.SliderCount_mob)})
    collection = Collection.objects.get(pk=1)
    collection_html = render_to_string('store/components/collection/collection.html',{'collection':collection})
    categories = Categorey.objects.all()
    # categorey_html = render_to_string('store/components/section/section.html',{'categorey':categorey.All_products.all(),'categorey_name':categorey.Name})
    render_context['topbar'] = topbar_html
    render_context['slider'] = slider_html
    render_context['collection'] = collection_html
    render_context['categories'] = categories
    render_context['brands'] = Brand.objects.all()
    return render(request,'store/index.html',render_context)

def product_view(request,ptype,p_id,v_id=None):
    render_context = {}
    if request.method == 'POST':
        print('POST Request')
    else:
        if 'query' in request.GET:
            last_variant = None
            all_variants = Variant.objects.filter(Product__id = p_id)
            
            for param in request.GET:
                if param != 'query':
                    if last_variant == None:
                        a = all_variants.filter(Attributevalue__Attribute__Name__contains = param.lower()).filter(Attributevalue__Value__contains = request.GET[param].lower())
                        last_variant = a
                    else:
                        a = last_variant.filter(Attributevalue__Attribute__Name__contains = param.lower()).filter(Attributevalue__Value__contains = request.GET[param].lower())
                        last_variant = a
            # print(last_variant[0].Name)
            # print(len(last_variant))
            if last_variant.exists():
                return HttpResponseRedirect(reverse('product_view',kwargs={'ptype':'variable','p_id':p_id,'v_id':last_variant[0].pk}))
            else:
                messages.warning(request,f"sorry! we current don't have that variant")
                return HttpResponseRedirect(request.path)
        else:
            # if normal product
            if ptype == 'normal':
                query_product = Product.objects.filter(pk=p_id).prefetch_related('Its_images')
                render_context['product'] = query_product[0]
                render_context['ptype'] = 'normal'
                render_context['attributes_detail'] = None
                #CHECK IF PRODUCT EXISTS IN CART IF AUTHENTICATED USER
                if request.user.is_authenticated:
                    if request.user.Customer.Cart.Cartproduct.filter(Product_id=p_id).exists():
                        render_context['In_cart'] = True
                    else:
                        render_context['In_cart'] = False
                else:
                    render_context['In_cart'] = False
                return render(request,'store/components/view/product/productView.html',render_context)
            # if product with Variant
            elif ptype == 'variable':
                query_product = ProductWithVariant.objects.filter(pk=p_id).prefetch_related('Variants__Attributevalue__Attribute').first()
                # Prepare Attribute Details
                render_context['attributes_detail'] = {}
                allVars = query_product.Variants.all()
                for variant in allVars:
                    variant_id = variant.id
                    for attribute_val in variant.Attributevalue.all():
                        attr = attribute_val.Attribute.Name
                        val = attribute_val.Value
                        if attr in render_context['attributes_detail'].keys():
                            if val not in render_context['attributes_detail'][attr]:
                                render_context['attributes_detail'][attr].append(val)
                        else:
                            render_context['attributes_detail'][attr] = [val]
                            # render_context['attributes_detail'][attr].append(val)
                render_context['product'] = query_product
                render_context['variant'] = query_product.Variants.filter(pk=v_id).prefetch_related('Images').first()
                render_context['ptype'] = 'variable'
                render_context['variant_vals'] = []
                for attrValue in render_context['variant'].Attributevalue.all():
                    render_context['variant_vals'].append(attrValue.Value)
                #CHECK IF VARIANT EXISTS IN CART IF AUTHENTICATED USER
                if request.user.is_authenticated:
                    if request.user.Customer.Cart.Cartvariant.filter(Variant_id=v_id).exists():
                        render_context['In_cart'] = True
                    else:
                        render_context['In_cart'] = False
                else:
                    render_context['In_cart'] = False
                # print(f'---------------{render_context["In_cart"]}-------------')
                # USE DJANGO SIGNAL TO CACHE THIS ATTRIBUTE DETAILS
                # print(render_context['attributes_detail'])
                return render(request,'store/components/view/product/productView.html',render_context)

def get_meta_data(request):
    if request.method == 'POST':
        recived_data = loads(request.body)
        print(recived_data)
        if recived_data['page'] == 'product' or 'productwithvariant':
            if recived_data['for'] == 'add':
                questions = Product_type.objects.get(pk=recived_data['pk']).Meta_data
                return HttpResponse(dumps({'list':questions}))
            else:
                productMetaData = Product.objects.get(pk=recived_data['pk']).Meta_data
                return HttpResponse(dumps(productMetaData))
        elif recived_data['page'] == 'product_type':
            questions = Product_type.objects.get(pk=recived_data['pk']).Meta_data
            return HttpResponse(dumps({'list':questions}))

def handle_product_search(request):
    if request.method == 'GET':
        render_context = {}
        if 'productquery' in request.GET and request.GET['productquery'] != '':
            # first check normal product match
            print('Searching Name')
            productquery = request.GET['productquery']
            all_normal_prods = Product.objects.filter(Name__icontains = productquery)
            all_variants = Variant.objects.filter(Name__icontains = productquery)
            if all_normal_prods.exists() or all_variants.exists():
                print('Name Exists')
                normal_prod_detail = all_normal_prods.values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Categorey_id','Is_normal_product')
                variable_prod_details = all_variants.values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Product_id','Is_normal_product')
                final_ordered_qs = variable_prod_details.union(normal_prod_detail,all=True).order_by('Cost_to_customer')
                # print(normal_prod_detail.union(variable_prod_details,all=True))
                # print(all_normal_prods.values('id','Categorey_id','Is_normal_product').union(all_variants.values('id','Product_id','Is_normal_product')))
                try:
                    page_no = request.GET['page']
                except:
                    page_no = 1
                
                try:
                    perpage = request.GET['perpage']
                except:
                    perpage = 2
                
                paginator = Paginator(final_ordered_qs, perpage,orphans=1)
                render_context['product_data'] = paginator.get_page(page_no)
                # only necassary in via text search (When searched through nav input)
                # only to let me know if there was any search result at all
                render_context['msg'] = True
                # only necassary in via text search (When searched through nav input)
                render_context['result_for'] = 'Name'
                render_context['productquery'] = productquery
                return render(request,'store/components/view/search/searchView.html',render_context)
            else:
                # No Match in Name
                # now match tags
                print('Searching Tags')
                all_tagged_normal_products = Product.objects.filter(Tags__Name__icontains = productquery).distinct().values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Categorey_id','Is_normal_product')
                all_tagged_variable_products = ProductWithVariant.objects.values('Variants').filter(Tags__Name__icontains = productquery).distinct().prefetch_related('Variants')
                prod_vars = None
                for product in all_tagged_variable_products:
                    p_vars = product.Variants.all().values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Product_id','Is_normal_product')
                    if prod_vars != None:
                        prod_vars = p_vars.union(prod_vars)
                    else:
                        prod_vars = p_vars
                prod_vars.union(all_tagged_normal_products).order_by('Cost_to_customer')
                if all_tagged_normal_products.exists():
                    print('Tags Exists')
                    render_context['product_data'] = all_tagged_normal_products
                    render_context['msg'] = True
                    render_context['result_for'] = 'Tags'
                    return render(request,'store/components/view/search/searchView.html',render_context)
                    # return Render
                else:
                    # No Match in Name  and Tags
                    # search Description
                    print('Searching Description')
                    all_tagged_normal_products = Product.objects.filter(Description__icontains = productquery).values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Categorey_id','Is_normal_product')
                    all_tagged_variable_products = ProductWithVariant.objects.filter(Description__icontains = productquery).prefetch_related('Variants')
                    prod_vars = None
                    for product in all_tagged_variable_products:
                        p_vars = product.Variants.all().values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Product_id','Is_normal_product')
                        if prod_vars != None:
                            prod_vars = p_vars.union(prod_vars)
                        else:
                            prod_vars = p_vars
                    prod_vars.union(all_tagged_normal_products).order_by('Cost_to_customer')
                    if all_tagged_normal_products.exists():
                        print('Description Exists')
                        render_context['product_data'] = all_tagged_normal_products
                        render_context['variant_details'] = prod_vars
                        render_context['msg'] = True
                        render_context['result_for'] = 'Description'
                        return render(request,'store/components/view/search/searchView.html',render_context)
                    else:
                        print('Final No result')
                        render_context['msg'] = False
                        render_context['result_for'] = None
                        return render(request,'store/components/view/search/searchView.html',render_context)
        elif request.GET['for'] == 'brandfilter':
            print(f'--------ID: {request.GET["querybrandId"]}---------')
            brandId = request.GET["querybrandId"]
            # BELOW TWO ARE FOR TESTING PURPOSES
            # all_normal_prods = Product.objects.filter(Brand_id=request.GET['querybrandId']).values('Is_normal_product','id')
            # all_variants = Variant.objects.filter(Product__Brand_id=request.GET['querybrandId']).select_related('Product').values('Is_normal_product','id')
            all_normal_prods = Product.objects.filter(Brand_id=request.GET['querybrandId']).values('Is_normal_product','id','Name','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Categorey_id','Meta_data')
            all_variants = Variant.objects.filter(Product__Brand_id=request.GET['querybrandId']).select_related('Product').values('Is_normal_product','id','Name','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Product_id','AttrCache')
            if all_normal_prods.exists() and all_variants.exists():
                # render_context['product_data'] contans
                # all Items (product+variant) details
                render_context['product_data'] = all_variants.union(all_normal_prods,all=True)
            else:
                if not all_normal_prods.exists() and not all_variants.exists():
                    render_context['product_data'] = all_normal_prods #Just any Empty Queryset
                elif not all_normal_prods.exists() and all_variants.exists():
                    render_context['product_data'] = all_variants
                elif all_normal_prods.exists() and not all_variants.exists():
                    render_context['product_data'] = all_normal_prods
            print(render_context['product_data'])
            render_context['msg'] = True
            render_context['result_for'] = 'brandfilter'
            # print(dfd)
            return render(request,'store/components/view/search/searchView.html',render_context)

        else:
            print('No Valid query!')
            render_context['msg'] = False
            render_context['result_for'] = None
            return render(request,'store/components/view/search/searchView.html',render_context)
    else:
        print('Error')
        return HttpResponse('<h1>Forbbiden</h1>')

def selected_variant(request,p_id,v_id):
    pass

def handleCart(request):
    if request.method == 'POST':
        print(request.POST)

def addItemToCart(request):
    if request.method == 'POST':
        recivedData = loads(request.body)
        print(recivedData)
        if(recivedData['ptype'] == 'variable'):
            # Implies have to add an Varinat to the cart
            # add items in variant
            if request.user.Customer.Cart.Cartvariant.all().filter(Variant_id=recivedData['variantId']).count() == 0:
                from datetime import datetime
                CartVariant.objects.create(
                    Variant = Variant.objects.get(pk = recivedData['variantId']),
                    Quantity = recivedData['quantity'],
                    Added = datetime.fromtimestamp(int(recivedData['time'])),
                    Cart = request.user.Customer.Cart
                )
                return HttpResponse('added',status=200)
            else:
                print('dublicate')
                return HttpResponse('dublicate')
        elif (recivedData['ptype'] == 'normal'):
            if Cart.objects.get(pk=request.user.Customer.Cart_id).Cartproduct.all().filter(Product_id = recivedData['productId']).count() == 0:
                from datetime import datetime
                CartProduct.objects.create(
                    Product = Product.objects.get(pk=recivedData['productId']),
                    Quantity = recivedData['quantity'],
                    Cart = request.user.Customer.Cart,
                    Added = datetime.fromtimestamp(int(recivedData['time']))
                )
                return HttpResponse('added',status=200)
            else:
                print('dublicate')
                return HttpResponse('dublicate')

@login_required
def viewCart(request):
    if request.method == "POST":
        data = loads(request.body)
        print(data)
        if data['ptype'] == 'normal':
            CartProduct.objects.filter(id=data['itemId']).delete()
        else:
            CartVariant.objects.filter(id=data['itemId']).delete()
    render_context = {}
    cartId = request.user.Customer.Cart_id
    # VERSION 1
    # cart = Cart.objects.prefetch_related('Cartproduct__Product','Cartvariant__Variant').get(pk = request.user.Customer.Cart_id)
    # allCartproducts = CartProduct.objects.filter(Cart_id = cart.id).select_related('Product')
    # allCartvariants = CartVariant.objects.filter(Cart_id = cart.id).select_related('Variant')
    # VERSION 2
    # allCartproducts = cart.Cartproduct.all().order_by('Added')
    # allCartvariants = cart.Cartvariant.all().order_by('Added')
    # VERSION 3
    # required to do annotation because Attrcache does not exist 
    # on product therfore tricked to get attrcache through "attributes" annotation
    allCartproducts = CartProduct.objects.annotate(attributes=F('Product__Meta_data')).filter(Cart_id = cartId).select_related('Product').values('id','Product__Is_variant','Product__Name','Product__Thumb_path','Product__Crossed_price','Product__Cost_to_customer','Quantity','Product__Discount','attributes','Added','Product_id','Product__id')
    allCartvariants = CartVariant.objects.annotate(attributes=F('Variant__AttrCache')).filter(Cart_id = cartId).select_related('Variant').values('id','Variant__Is_variant','Variant__Name','Variant__Thumb_path','Variant__Crossed_price','Variant__Cost_to_customer','Quantity','Variant__Discount','attributes','Added','Variant__id','Variant__Product_id')
    # allCartProd = CartProduct.objects.Product.all()
    # for product in allCartProd:
    #     product
    # allCartVar = CartVariant.objects.Variant.all()
    # TESTING VERSION
    # allCartproducts = CartProduct.objects.annotate(ptype='product').filter(Cart_id = cartId).select_related('Products').values('Product__Is_variant','Added')
    # allCartvariants = CartVariant.objects.annotate(ptype='variant').filter(Cart_id = cartId).select_related('Variant').values('Variant__Is_variant','Added')
    # allProds = []
    # allVars = []
    # for cartprod in allCartproducts:
    #     product = cartprod.Product
    #     allProds.append(product)
    # for cartvar in allCartvariants:
    #     variant = cartvar.Variant
    #     allVars.append(variant)
    
    # allItems = allCartproducts.union(allCartvariants,all=True).order_by('Added')
    render_context['allItems'] = allCartvariants.union(allCartproducts,all=True).order_by('-Added')
    try:
        render_context['total_amt_customer'] = sum([Item['Variant__Cost_to_customer'] for Item in render_context['allItems']])
        render_context['total_amt_crossed'] = sum([Item['Variant__Crossed_price'] for Item in render_context['allItems']])
        render_context['saved_amt'] = render_context['total_amt_crossed'] - render_context['total_amt_customer']
        render_context['saved_amt_percent'] = round(((render_context['saved_amt'])/render_context['total_amt_crossed'])*100)
    except:
        render_context['total_amt_customer'] = 0
        render_context['total_amt_crossed'] = 0
        render_context['saved_amt_percent'] = 0
    render_context['numItems'] = render_context['allItems'].count()
    # print(allItems)
    else:
        
    return render(request,'store/components/view/cart/baseCart.html',render_context)

@login_required
def orderpage(request):
    if request.user.is_authenticated:
        cartId = request.user.Customer.Cart_id
        print(cartId)
        allCartprods = CartProduct.objects.filter(Cart_id=cartId).exists()
        allCartvars = CartVariant.objects.filter(Cart_id = cartId).exists()
        if allCartprods or allCartvars:
            # proceed as normal, start address selection process
            render_context = {}
            allCartproducts = CartProduct.objects.filter(Cart_id = cartId).select_related('Product').values('Product__Crossed_price','Product__Cost_to_customer')
            allCartvariants = CartVariant.objects.filter(Cart_id = cartId).select_related('Variant').values('Variant__Crossed_price','Variant__Cost_to_customer')
            render_context['allItems'] = allCartvariants.union(allCartproducts,all=True)
            render_context['total_amt_customer'] = sum([Item['Variant__Cost_to_customer'] for Item in render_context['allItems']])
            render_context['total_amt_crossed'] = sum([Item['Variant__Crossed_price'] for Item in render_context['allItems']])
            render_context['saved_amt'] = render_context['total_amt_crossed'] - render_context['total_amt_customer']
            render_context['saved_amt_percent'] = round(((render_context['saved_amt'])/render_context['total_amt_crossed'])*100)
        else:
            render_context = {}
            render_context['allItems'] = []
            render_context['total_amt_customer'] = 0
            render_context['total_amt_crossed'] = 0
            render_context['saved_amt_percent'] = 0
            render_context['numItems'] = 0
        if request.method == 'POST':
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                savedInstance = form.save(commit=False)
                savedInstance.Owner = request.user.Customer
                savedInstance.save()
                # MORE LOGIC WILL BE WRITTEN
                return HttpResponse('SUCCESS')
            else:
                render_context['form'] = form
                return render(request,'store/components/order/orderPage.html',render_context)
        else:
            render_context['form'] = ShippingAddressForm()
            return render(request,'store/components/order/orderPage.html',render_context)
    else:
        # redirect to the login page
        return HttpResponse('<h1>Forbidden Page,No Logged In</h1>')

def asyncsearch(request):
    if request.method == 'POST':
        allVariants = Variant.objects.all().values_list('id','Name')
        varList = []
        for variant in allVariants:
            varList.append({'id':variant[0],'name':variant[1],'ptype':'variable'})
        return JsonResponse({"matchedItems":varList})
    else:
        allVariants = Variant.objects.all().values_list('id','Name','Product_id')
        varList = []
        for variant in allVariants:
            varList.append({'v_id':variant[0],'name':f'{variant[1]}....','p_id':variant[2],'ptype':'variable'})
        return JsonResponse({"matchedItems":varList})

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("customer_login"))

def handle_login(request):
    if request.method == 'POST':
        formData = LoginForm(request.POST)
        if formData.is_valid():
            from django.contrib.auth import login, authenticate
            user = authenticate(username=formData.cleaned_data['Username'],password=formData.cleaned_data.get('Password'))
            if user != None:
                login(request,user)
                messages.success(request,'Login Successful')
                return HttpResponseRedirect(reverse('viewcart'))
            else:
                render_context = {}
                render_context['form'] = LoginForm()
                messages.error(request,'Invalid Details!')
                return render(request,'store/components/user/login.html',render_context)
    else:
        render_context = {}
        render_context['form'] = LoginForm()
        return render(request,'store/components/user/login.html',render_context)


def handle_register(request):
    if request.method == 'POST':
        formData = CustomUserCreationForm(request.POST)
        if formData.is_valid():
            new_user = formData.save()
            new_user.refresh_from_db()
            new_user.Customer.PhoneNumber = formData.cleaned_data.get('PhoneNumber')
            new_user.save()
            raw_pass = formData.clean_password2()
            from django.contrib.auth import login, authenticate
            user = authenticate(username=formData.cleaned_data['username'],password=formData.clean_password2())
            login(request,user)
            messages.info(request,f'You have registered successfully With username: {formData.cleaned_data.get("username")}')
            return HttpResponseRedirect(reverse('login'))
            # new_user.save() #signal will automatically create and attach customer instance
            # # new_user.refresh_from_db() #now will be able to acess Customer profile
        else:
            return render(request,'store/components/user/register.html',{ 'form' : formData })
        print('got POST')
        print(request.POST)
    else:
        return render(request,'store/components/user/register.html',{ 'form' : CustomUserCreationForm() })


# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# OLD SEARCH IMPLEMENTATIONS SAVED SNIPPETS
# only necassary in via text search (When searched through nav input)
            # all_normal_prods = Product.objects.filter(Name__icontains = productquery)
            # all_variants = Variant.objects.filter(Name__icontains = productquery)
            # if all_normal_prods.exists() or all_variants.exists():
            #     print('Name Exists')
            #     normal_prod_detail = all_normal_prods.values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Brand_id','Is_normal_product')
            #     variable_prod_details = all_variants.values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Product_id','Is_normal_product')
            #     final_ordered_qs = variable_prod_details.union(normal_prod_detail,all=True).order_by('Cost_to_customer')
            #     # print(normal_prod_detail.union(variable_prod_details,all=True))
            #     # print(all_normal_prods.values('id','Brand_id','Is_normal_product').union(all_variants.values('id','Product_id','Is_normal_product')))
            #     try:
            #         page_no = request.GET['page']
            #     except:
            #         page_no = 1
                
            #     try:
            #         perpage = request.GET['perpage']
            #     except:
            #         perpage = 2
                
            #     paginator = Paginator(final_ordered_qs, perpage,orphans=1)
            #     render_context['product_data'] = paginator.get_page(page_no)
            #     # only necassary in via text search (When searched through nav input)
            #     # only to let me know if there was any search result at all
            #     render_context['msg'] = True
            #     # only necassary in via text search (When searched through nav input)
            #     render_context['result_for'] = 'Name'
            #     render_context['productquery'] = productquery
            #     return render(request,'store/components/view/search/searchView.html',render_context)
            # else:
            #     # No Match in Name  and Tags
            #     # search Description
            #     print('Searching Description')
            #     all_tagged_normal_products = Product.objects.filter(Description__icontains = productquery).values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Brand_id','Is_normal_product')
            #     all_tagged_variable_products = ProductWithVariant.objects.filter(Description__icontains = productquery).prefetch_related('Variants')
            #     prod_vars = None
            #     for product in all_tagged_variable_products:
            #         p_vars = product.Variants.all().values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Product_id','Is_normal_product')
            #         if prod_vars != None:
            #             prod_vars = p_vars.union(prod_vars)
            #         else:
            #             prod_vars = p_vars
            #     prod_vars.union(all_tagged_normal_products).order_by('Cost_to_customer')
            #     if all_tagged_normal_products.exists():
            #         print('Description Exists')
            #         render_context['product_data'] = all_tagged_normal_products
            #         render_context['variant_details'] = prod_vars
            #         render_context['msg'] = True
            #         render_context['result_for'] = 'Description'
            #         return render(request,'store/components/view/search/searchView.html',render_context)
            #     else:
            #         print('Final No result')
            #         render_context['msg'] = False
            #         render_context['result_for'] = None
            #         return render(request,'store/components/view/search/searchView.html',render_context)