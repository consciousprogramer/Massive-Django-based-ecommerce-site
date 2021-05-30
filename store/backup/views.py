from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import F,Value,Q,prefetch_related_objects,Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from . models import *
from json import loads,dumps
from .forms import ShippingAddressForm,RegisterForm,LoginForm,CustomUserCreationForm
from django.conf import settings
from Paytm import Checksum
# Create your views here.

def index(request):
    render_context = {}
    topbar = TopBar.objects.filter(Active=True).prefetch_related('Images').first()
    topbar_html = render_to_string('store/components/Topbar/topbar.html',{'topbar_images':topbar.Images.all()})
    slider = Slider.objects.filter(Active=True).prefetch_related('Slide_pc','Slide_mob').first()
    slider_html = render_to_string('store/components/slider/slider.html',{'slides_pc':slider.Slide_pc.all(),'slides_mob':slider.Slide_mob.all(),'sliderCount_pc':range(0,slider.SliderCount_pc),'sliderCount_mob':range(0,slider.SliderCount_mob)})
    collections = Collection.objects.filter(Show_on_mainpage=True).prefetch_related('Products','Variants')
    ctt = []
    for collection in collections:
        a = {
            'collection_name':[collection.pk,collection.Name,collection.Description],
            'collection_items':collection.Variants.all().values_list('Is_variant','Thumb_path','id','Product_id','Name','Cost_to_customer','Crossed_price','Discount').union(collection.Products.all().values_list('Is_variant','Thumb_path','id','Brand_id','Name','Cost_to_customer','Crossed_price','Discount')),
        }
        ctt.append(a)
    collection_html = render_to_string('store/components/collection/collection.html',{'all_collection':ctt})
    # categories = Categorey.objects.all()
    productRows = ProductRow.objects.filter(Show_on_mainpage=True).prefetch_related('Products','Variants')
    att = []
    for row in productRows:
        a = {
            'rowName':[row.pk,row.Name],
            'rowItems':row.Variants.all().values_list('Is_variant','Thumb_path','id','Product_id','Name','Cost_to_customer','Crossed_price','Discount').union(row.Products.all().values_list('Is_variant','Thumb_path','id','Brand_id','Name','Cost_to_customer','Crossed_price','Discount')),
        }
        n=5
        for i in range(n):
            att.append(a)
    banner = Banner.objects.filter(Active=True).first()
    # render_context['rowData'].append({
    #     'rowName':[row.pk,row.Name],
    #     'rowItems':row.Variants.all().values_list('Is_variant','Thumb_path','id','Product_id','Name','Cost_to_customer','Crossed_price','Discount').union(row.Products.all().values_list('Is_variant','Thumb_path','id','Brand_id','Name','Cost_to_customer','Crossed_price','Discount')),
    # })
    # categorey_html = render_to_string('store/components/section/section.html',{'categorey':categorey.All_products.all(),'categorey_name':categorey.Name})
    render_context['topbar'] = topbar_html
    render_context['slider'] = slider_html
    render_context['collection'] = collection_html
    render_context['brands'] = Brand.objects.all()
    render_context['allRowdata'] = att
    render_context['Banner'] = banner
    # print(sds)
    return render(request,'store/index.html',render_context)

def product_view(request,ptype,p_id,v_id=None):
    render_context = {}
    if request.method == 'POST':
        data = loads(request.body)
        if data['for'] == 'viewed':
            try:
                varList = request.session['varstr']
                varList = varList.split('-')
            except:
                varList = []
            try:
                prodList = request.session['prodstr']
                prodList = prodList.split('-')
            except:
                prodList =[]
            allProds = Product.objects.filter(pk__in=prodList).values_list('Is_variant','Thumb_path','id','Brand_id','Name','Cost_to_customer','Crossed_price','Discount')
            allVars = Variant.objects.filter(pk__in=varList).values_list('Is_variant','Thumb_path','id','Product_id','Name','Cost_to_customer','Crossed_price','Discount')
            rowData = {
                'rowName':[1,f'Recently Viewed Products ({len(varList)+len(prodList)} Item)'],
                'rowItems': allVars.union(allProds)
            }
            viewed_html = render_to_string('store/components/ajax/viewed.html',{'rowdata':rowData})
            return HttpResponse(viewed_html)
        if data['for'] == 'recommend':
            items = set()
            if ptype == 'normal':
                # prod = Product.objects.filter(pk=p_id).only('Tags','Tags__All_taged_products__Is_variant','Tags__All_taged_products__id','Tags__All_taged_products__Name','Tags__All_taged_products__Cost_to_customer','Tags__All_taged_products__Crossed_price','Tags__All_taged_products__Discount','Tags__All_taged_products__Brand_id','Tags__All_products_with_variant__id','Tags__All_products_with_variant__Variants__id','Tags__All_products_with_variant__Variants__Is_variant','Tags__All_products_with_variant__Variants__Name','Tags__All_products_with_variant__Variants__Cost_to_customer','Tags__All_products_with_variant__Variants__Crossed_price','Tags__All_products_with_variant__Variants__Discount','Tags__All_products_with_variant__Variants__Thumb_path').prefetch_related('Tags__All_taged_products','Tags__All_products_with_variant').first()
                prod = Product.objects.filter(pk=p_id).prefetch_related('Tags__All_taged_products','Tags__All_products_with_variant').first()
                print(f'prod-{prod}')
                for tag in prod.Tags.all():
                    for item in tag.All_taged_products.all():
                        items.add(item)
                    for item in tag.All_products_with_variant.all():
                        items.add(item.Variants.all().first())
            elif ptype == 'variable':
                prod = ProductWithVariant.objects.filter(pk=p_id).prefetch_related('Tags__All_taged_products','Tags__All_products_with_variant').first()
                for tag in prod.Tags.all():
                    for item in tag.All_taged_products.all():
                        items.add(item)
                    for item in tag.All_products_with_variant.all():
                        items.add(item.Variants.all().first())
            print(items)
            recommended_html = render_to_string('store/components/ajax/recommend.html',{'items':items})
            return HttpResponse(recommended_html)
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
                # print("updating_viewed")
                if 'prodstr' in request.session:
                    backup = request.session['prodstr']
                    if str(p_id) not in backup.split('-'):
                        backup += f'-{p_id}'
                        request.session['prodstr'] = backup
                else:
                    request.session['prodstr'] = str(p_id)
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
                print(f'---------------{render_context["In_cart"]}-------------')
                # USE DJANGO SIGNAL TO CACHE THIS ATTRIBUTE DETAILS
                # print(render_context['attributes_detail'])
                print("updating_viewed")
                if 'varstr' in request.session:
                    backup = request.session['varstr']
                    if str(v_id) not in backup.split('-'):
                        backup += f'-{v_id}'
                        request.session['varstr'] = backup
                else:
                    request.session['varstr'] = str(v_id)
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
    from django.contrib.postgres.search import SearchQuery,SearchVector
    if request.method == 'GET':
        render_context = {}
        if 'productquery' in request.GET:
            if request.GET['productquery'] != ("" or " "):
                # first check normal product match
                print('Searching Name')
                productquery = request.GET['productquery']
                allItems = []
                sv  = SearchVector('Name','Description')
                sq = SearchQuery(productquery)
                allProds = Product.objects.annotate(
                    search=sv
                ).filter(
                    search=sq
                ).values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Brand_id','Is_normal_product')

                allVars = Variant.objects.annotate(
                    search=sv
                ).filter(
                    search=sq
                ).values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Product_id','Is_normal_product','AttrCache')
                
                for prod in allProds:
                    allItems.append(prod)
                for var in allVars:
                    allItems.append(var)
                if allItems:
                    try:
                        page_no = request.GET['page']
                    except:
                        page_no = 1
                    
                    try:
                        perpage = request.GET['perpage']
                    except:
                        perpage = 2
                    paginator = Paginator(allItems,perpage,orphans=1)
                    render_context['product_data'] = paginator.get_page(page_no)
                    render_context['msg'] = True
                    render_context['result_for'] = 'Name'
                    render_context['productquery'] = productquery
                    return render(request,'store/components/view/search/searchView.html',render_context)
                else:
                    allItems = []
                    sv = SearchVector('Tags__Name')
                    sq = SearchQuery(productquery)
                    allProds = Product.objects.annotate(
                        search=sv
                    ).filter(
                        search=sq
                    ).values('Name','id','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Brand_id','Is_normal_product')
                    allVars = ProductWithVariant.objects.prefetch_related(Prefetch('Variants',to_attr='its_var')).annotate(
                        search=sv
                    ).filter(
                        search=sq
                    ).values('id','Variants')
                    for prod in allProds:
                        allItems.append(prod)
                    try:
                        for item in allVars.its_var:
                            for var in item.its_var:
                                allItems.append(var)
                                # allItems.append(var)
                    except:
                        pass
                    if allItems:
                        try:
                            page_no = request.GET['page']
                        except:
                            page_no = 1
                        
                        try:
                            perpage = request.GET['perpage']
                        except:
                            perpage = 2
                        paginator = Paginator(allItems,perpage,orphans=1)
                        render_context['product_data'] = paginator.get_page(page_no)
                        render_context['msg'] = True
                        render_context['result_for'] = 'Name'
                        render_context['productquery'] = productquery
                        return render(request,'store/components/view/search/searchView.html',render_context)
                    else:
                        messages.warning(request, f'Sorry No result found for "{productquery}"')
                        paginator = Paginator(allItems,2,orphans=1)
                        render_context['product_data'] = paginator.get_page(1)
                        render_context['msg'] = False
                        render_context['result_for'] = None
                        render_context['productquery'] = productquery
                        return render(request,'store/components/view/search/searchView.html',render_context)
            else:
                paginator = Paginator(allItems,2,orphans=1)
                render_context['product_data'] = paginator.get_page(1)
                render_context['msg'] = False
                render_context['result_for'] = None
                render_context['productquery'] = 'Empty search'
                return render(request,'store/components/view/search/searchView.html',render_context)
        elif request.GET['for'] == 'categoreyfilter':
            pass
        elif request.GET['for'] == 'brandfilter':
            print(f'--------ID: {request.GET["querybrandId"]}---------')
            brandId = request.GET["querybrandId"]
            # BELOW TWO ARE FOR TESTING PURPOSES
            # all_normal_prods = Product.objects.filter(Brand_id=request.GET['querybrandId']).values('Is_normal_product','id')
            # all_variants = Variant.objects.filter(Product__Brand_id=request.GET['querybrandId']).select_related('Product').values('Is_normal_product','id')
            all_normal_prods = Product.objects.filter(Brand_id=request.GET['querybrandId']).values('Is_normal_product','id','Name','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Brand_id','Meta_data')
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
        elif request.GET['for'] == 'collection':
            c_id = request.GET['col_id']
            query_collection = Collection.objects.get(pk = c_id)
            prefetch_related_objects([query_collection],'Products','Variants')
            allProds = query_collection.Products.all().values('Is_normal_product','id','Name','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Brand_id','Meta_data')
            allVars = query_collection.Variants.all().values('Is_normal_product','id','Name','Cost_to_customer','Crossed_price','Thumb_path','Highlights','Discount','Product_id','AttrCache')
            render_context['product_data'] = allVars.union(allProds)
            render_context['msg'] = True
            render_context['result_for'] = 'collection'
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
                # why
                if 'items' in request.session:
                    # varList keeps record of all cart variants
                    backup = request.session['items']
                    backup['varList'].append(recivedData['variantId'])
                    request.session['items'] = backup
                    print('added varlist try')
                    print(request.session['items'])
                else:
                    backup = {'varList':[],'prodList':[]}
                    backup['varList'].append(recivedData['variantId'])
                    request.session['items'] = backup
                    print('added varlist except')
                    print(request.session['items'])
                return HttpResponse('added',status=200)
            else:
                print('dublicate')
                return HttpResponse('dublicate')
        elif recivedData['ptype'] == 'normal':
            if Cart.objects.get(pk=request.user.Customer.Cart_id).Cartproduct.all().filter(Product_id = recivedData['productId']).count() == 0:
                from datetime import datetime
                CartProduct.objects.create(
                    Product = Product.objects.get(pk=recivedData['productId']),
                    Quantity = recivedData['quantity'],
                    Cart = request.user.Customer.Cart,
                    Added = datetime.fromtimestamp(int(recivedData['time']))
                )
                if 'prodList' in request.session:
                    backup = request.session['items']
                    backup['prodList'].append(recivedData['productId'])
                    request.session['items'] = backup
                    print('added prodlist try')
                    print(request.session['items'])
                else:
                    backup = {'varList':[],'prodList':[]}
                    backup['prodList'].append(recivedData['productId'])
                    request.session['items'] = backup
                    print('added prodlist except')
                    print(request.session['items'])
                return HttpResponse('added',status=200)
            else:
                print('dublicate')
                return HttpResponse('dublicate')


def viewCart(request):
    if request.method == 'UPDATE':
        data = loads(request.body)
        if data['ptype'] == 'normal':
            a = CartProduct.objects.get(id=data['itemId'])
            if data['changeType'] == 'plus':
                a.Quantity = a.Quantity + int(data['change'])
            else:
                a.Quantity = a.Quantity - int(data['change'])
            a.save(update_fields=['Quantity'])
            messages.success(request,'Item quantity upadted successfully')
            return HttpResponse(status=200)
        else:
            a = CartVariant.objects.get(pk=data['itemId'])
            if data['changeType'] == 'plus':
                a.Quantity = a.Quantity + int(data['change'])
            else:
                a.Quantity = a.Quantity - int(data['change'])
            a.save(update_fields=['Quantity'])
            messages.success(request,'Item quantity upadted successfully')
            return HttpResponse(status=200)
        return HttpResponse(status=500)
    elif request.method == "POST":
        if request.user.is_authenticated:
            data = loads(request.body)
            print(data)
            if data['ptype'] == 'normal':
                a = CartProduct.objects.get(id=data['itemId'])
                prodId = a.Product_id
                a.delete()
                backup = request.session['items']
                print(backup)
                backup['prodList'].remove(str(prodId))
                request.session['items'] = backup
                del a
                print('removed from session')
                return HttpResponse(status=200)
            else:
                a = CartVariant.objects.get(id=data['itemId'])
                varId = a.Variant_id
                a.delete()
                backup = request.session['items']
                backup['varList'].remove(str(varId))
                request.session['items'] = backup
                del a
                print('removed from session')
                return HttpResponse(status=200)
    else:
    # if get request
        # if get request of authed user,no query params reqired
        if request.user.is_authenticated:
            render_context = {}
            cartId = request.user.Customer.Cart_id
            allCartproducts = CartProduct.objects.annotate(attributes=F('Product__Meta_data')).filter(Cart_id = cartId).select_related('Product').values('id','Product__Is_variant','Product__Name','Product__Thumb_path','Product__Crossed_price','Product__Cost_to_customer','Quantity','Product__Discount','attributes','Added','Product_id','Product__id')
            allCartvariants = CartVariant.objects.annotate(attributes=F('Variant__AttrCache')).filter(Cart_id = cartId).select_related('Variant').values('id','Variant__Is_variant','Variant__Name','Variant__Thumb_path','Variant__Crossed_price','Variant__Cost_to_customer','Quantity','Variant__Discount','attributes','Added','Variant__id','Variant__Product_id')
            render_context['allItems'] = allCartvariants.union(allCartproducts,all=True).order_by('-Added')
            if render_context['allItems'].exists():
                render_context['total_amt_customer'] = sum([Item['Variant__Cost_to_customer']*Item['Quantity'] for Item in render_context['allItems']])
                render_context['total_amt_crossed'] = sum([Item['Variant__Crossed_price']*Item['Quantity'] for Item in render_context['allItems']])
                render_context['saved_amt'] = render_context['total_amt_crossed'] - render_context['total_amt_customer']
                render_context['saved_amt_percent'] = round(((render_context['saved_amt'])/render_context['total_amt_crossed'])*100)
            else:
                render_context['total_amt_customer'] = 0
                render_context['total_amt_crossed'] = 0
                render_context['saved_amt'] = 0
                render_context['saved_amt_percent'] = 0
            render_context['numItems'] = render_context['allItems'].count()
        else:
            messages.debug(request,'Not authed user')
            # if get request of un_authed user
            # check query params for varlist and prodlist
            if 'varlist' in request.GET or 'prodlist' in request.GET:
                messages.debug(request,'Have queryparams')
                if 'varlist' in request.GET:
                    var_details_list = request.GET['varlist'].split('-')
                    # key-value of varid and quantity
                    vardict = {}
                    for el in var_details_list:
                        a = el.split('_')
                        vardict[a[0]] = int(a[1])
                    print(vardict)
                    allVars = Variant.objects.filter(pk__in=vardict.keys()).values_list('Is_variant','id','Product_id','Name','Thumb_path','Cost_to_customer','Crossed_price','Discount','AttrCache')
                else:
                    allVars = []
                if 'prodlist' in request.GET:
                    prod_details_list = request.GET['prodlist'].split('-')
                    # key-value of prodid and quantity
                    # {id:quantity}
                    proddict = {}
                    for el in prod_details_list:
                        a = el.split('_')
                        # print(type(a[0]))->str
                        # print(type(a[1]))->str
                        proddict[a[0]] = int(a[1])
                    print(proddict)
                    allProds = Product.objects.filter(pk__in=proddict.keys()).values_list('Is_variant','id','Brand_id','Name','Thumb_path','Cost_to_customer','Crossed_price','Discount','Meta_data')
                else:
                    allProds = []
                # ----------------
                render_context = {}
                render_context['allItems'] = []
                for prod in allProds:
                    # prod[1] ==> prod id
                    # proddict[str(prod[1])] ==> prod quantity
                    p_quant = proddict[str(prod[1])]
                    render_context['allItems'].append(prod + (p_quant,p_quant*prod[5],p_quant*prod[6]))
                for var in allVars:
                    q_quant = vardict[str(var[1])]
                    render_context['allItems'].append(var + (q_quant,q_quant*var[5],q_quant*var[6]))
                # print(render_context['allItems'])
                render_context['total_amt_customer'] = sum([item[10] for item in render_context['allItems']])
                render_context['total_amt_crossed'] = sum([item[11] for item in render_context['allItems']])
                render_context['saved_amt'] = render_context['total_amt_crossed'] - render_context['total_amt_customer']
                render_context['saved_amt_percent'] = round(((render_context['saved_amt'])/render_context['total_amt_crossed'])*100)
                render_context['numItems'] = len(render_context['allItems'])
            else:
                messages.debug(request,'No queryparams')
                # if get req of un_authed and no query params
                render_context = {
                    'allItems' : [],
                    'total_amt_customer' : 0,
                    'total_amt_crossed' : 0,
                    'saved_amt_percent' : 0,
                    'numItems' : 0,
                }
        return render(request,'store/components/view/cart/baseCart.html',render_context)

def select_payment_gateway(request):
    # this view will instanciate & handle payments
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Get the method and
            # Iniciate the appropriate paymet preocess
            # Actually there no need for post request
            print('Post Method In Payments view')
            pass
        else:
            if 'for' not in request.GET:
                # ACTUALLY THIS IS USELESS PAGE,SOLVES NO PURPOSE
                cartId = request.user.Customer.Cart_id
                allCartproducts = CartProduct.objects.filter(Cart_id = cartId).select_related('Product').values('Product__Crossed_price','Product__Cost_to_customer','Quantity')
                allCartvariants = CartVariant.objects.filter(Cart_id = cartId).select_related('Variant').values('Variant__Crossed_price','Variant__Cost_to_customer','Quantity')
                if allCartproducts.count() > 0 or allCartvariants.count() > 0:
                    render_context = {}
                    render_context['allItems'] = allCartvariants.union(allCartproducts,all=True)
                    render_context['total_amt_customer'] = sum([Item['Variant__Cost_to_customer']*Item['Quantity'] for Item in render_context['allItems']])
                    render_context['total_amt_crossed'] = sum([Item['Variant__Crossed_price']*Item['Quantity'] for Item in render_context['allItems']])
                    render_context['saved_amt'] = render_context['total_amt_crossed'] - render_context['total_amt_customer']
                    render_context['saved_amt_percent'] = round(((render_context['saved_amt'])/render_context['total_amt_crossed'])*100)
                else:
                    render_context = {}
                    render_context['allItems'] = []
                    render_context['total_amt_customer'] = 0
                    render_context['total_amt_crossed'] = 0
                    render_context['saved_amt_percent'] = 0
                    render_context['numItems'] = 0
                render_context['allMethods'] = PaymentMethod.objects.all()
                return render(request,'store/components/order/selectMethod.html',render_context)
            elif request.GET['for'] == 'proceed-for-payment':
                if request.user.is_authenticated:
                    cartId =  request.user.Customer.Cart_id
                    custId = request.user.Customer.id
                    allCartproducts = CartProduct.objects.filter(Cart_id = cartId).select_related('Product')
                    allCartvariants = CartVariant.objects.filter(Cart_id = cartId).select_related('Variant')
                    currShippingAddress = ShippingAddress.objects.get(pk=request.session['this_order_shipadd_id_willbe'])
                    created_order = Order.objects.create(
                        Customer=request.user.Customer,
                        ShippingAddress=currShippingAddress,
                        Status='0',
                        TotalPrice=0,
                        Method=PaymentMethod.objects.all().first()
                    )
                    if allCartproducts.exists() or allCartvariants.exists():
                        Total = 0
                        # print(fghfg)
                        for cartprod in allCartproducts:
                            OrderProduct.objects.create(
                                Product=cartprod.Product,
                                Order=created_order,
                                Quantity=cartprod.Quantity
                            )
                            Total += cartprod.Product.Cost_to_customer*cartprod.Quantity
                        for cartvar in allCartvariants:
                            OrderVariant.objects.create(
                                Variant=cartvar.Variant,
                                Order=created_order,
                                Quantity=cartvar.Quantity
                            )
                            Total += cartvar.Variant.Cost_to_customer*cartvar.Quantity
                        # For NOW NOT DELETEING CART ITEMS BUT DELETE LATER
                        created_order.TotalPrice = Total
                        created_order.save(update_fields=['TotalPrice'])
                        Phnum = currShippingAddress.PhoneNumber

                        # Finished majar part
                        ORDER_ID = created_order.pk
                        param_dict = {
                            'MID': settings.PAYTM_MERCHANT_ID,
                            'ORDER_ID': str(ORDER_ID),
                            'TXN_AMOUNT': str(Total),
                            'CUST_ID': str(custId),
                            'INDUSTRY_TYPE_ID': 'Retail',
                            'WEBSITE': 'WEBSTAGING',
                            'CHANNEL_ID': 'WEB',
                            'MOBILE_NO':str(Phnum),
                            'CALLBACK_URL':'http://127.0.0.1:8000/paytm_response/',
                        }
                        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.PAYTM_MERCHANT_KEY)
                        print(param_dict)
                        return render(request,'store/paytm.html',{'param_dict':param_dict})
                    else:
                        messages.error(request,'You have no item in your cart,please add items then checkout!')
                        return HttpResponseRedirect(reverse('cartview'))


@login_required
def orderpage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                savedInstance = form.save(commit=False)
                savedInstance.Owner = request.user.Customer
                savedInstance.save()
                messages.success(request,'New Address Added Successfully For the user!')
                # this only happen when user place order for first time
                request.session['this_order_shipadd_id_willbe'] = savedInstance.pk
                # MORE LOGIC WILL BE WRITTEN
                # procces for payment method selection
                return HttpResponseRedirect(reverse('select_payment_gateway'))
                # convert cartitems to order items
            else:
                render_context['form'] = form
                return render(request,'store/components/order/orderPage.html',render_context)
        else:
            # THIS else deals with cart conversion
            if 'in_transition' in request.session:
                if 'register_complete' in request.session:
                    if request.session['register_complete']:
                        if 'with_cart' in request.GET:
                            # acess session.cart and
                            # now populated user's cart
                            # but before this check if user have any items in db cart
                            # if yes update it with session.cart.item.Quantity
                            usercart = request.user.Customer.Cart
                            cid = request.user.Customer.Cart_id
                            cartProds = CartProduct.objects.filter(Cart=usercart)
                            cartVars = CartVariant.objects.filter(Cart=usercart)
                            if cartVars.exists():
                                vardict = {}
                                for var in cartvars:
                                    vardict[str(var.pk)] = var.Quantity
                            if cartProds.exists():
                                proddict = {}
                                for prod in cartProds:
                                    proddict[str(prod.pk)] = prod.Quantity
                            
                            raw_cart = dict(request.session['cart'])
                            for item in raw_cart:
                                if item['ptype'] == 'normal':
                                    # create Cartproduct
                                    if item['productId'] in proddict.keys():
                                        a = cartProds.filter(Product_id=item['productId']).first()
                                        a.Quantity = proddict[item['productId']]
                                        a.save(update_fields=['Quantity'])
                                    else:
                                        CartProduct.objects.create(Cart_id=cid,Product_id=item['productId'],Quantity=item['quantity'])
                                else:
                                    # create Cartvariant
                                    if item['variantId'] in vardict.keys():
                                        a = cartVars.filter(Variant_id=item['variantId']).first()
                                        a.Quantity = vardict[item['variantId']]
                                        a.save(update_fields=['Quantity'])
                                    else:
                                        CartVariant.objects.create(Cart_id=cid,Variant_id=item['variantId'],Quantity=item['quantity'])
                            # clear all transition related session data as transition from un-auth to authed is complete
                            del request.session['in_transition']
                            del request.session['register_complete']
                            return HttpResponseRedirect(reverse('viewcart'))
                        else:
                            # contains script which will send cart to server
                            print(f'--------- CONVERTING CART--------')
                            return render(request,'store/components/order/convertCart.html',{
                                'page':'register'
                            })
                    else:
                        messages.warning(request,'Please complete Login/Register process, you have left in between!')
                        return HttpResponseRedirect(reverse('register'))
            else:
                # noraml get request for the orderpage,recall what is ??
                cartId = request.user.Customer.Cart_id
                print(cartId)
                allCartproducts = CartProduct.objects.filter(Cart_id = cartId).select_related('Product').values('Product__Crossed_price','Product__Cost_to_customer','Quantity')
                allCartvariants = CartVariant.objects.filter(Cart_id = cartId).select_related('Variant').values('Variant__Crossed_price','Variant__Cost_to_customer','Quantity')
                if allCartproducts.count() > 0 or allCartvariants.count() > 0:
                    # proceed as normal, start address selection process
                    render_context = {}
                    render_context['allItems'] = allCartvariants.union(allCartproducts,all=True)
                    render_context['total_amt_customer'] = sum([Item['Variant__Cost_to_customer']*Item['Quantity'] for Item in render_context['allItems']])
                    render_context['total_amt_crossed'] = sum([Item['Variant__Crossed_price']*Item['Quantity'] for Item in render_context['allItems']])
                    render_context['saved_amt'] = render_context['total_amt_crossed'] - render_context['total_amt_customer']
                    render_context['saved_amt_percent'] = round(((render_context['saved_amt'])/render_context['total_amt_crossed'])*100)
                else:
                    messages.error(request,'No item in your cart, add items and try again!')
                    return HttpResponseRedirect(reverse('viewcart'))
                render_context['form'] = ShippingAddressForm()
                render_context['allAddress'] = ShippingAddress.objects.filter(Owner_id=request.user.Customer.id)
                return render(request,'store/components/order/orderPage.html',render_context)
    else:
        # redirect to the login page
        return HttpResponse('<h1>Forbidden Page, For Authenticated users only!</h1>')

def select_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
        else:
            if 'withaddress' in request.GET:
                request.session['this_order_shipadd_id_willbe'] = request.GET['withaddress']
                # Not sense to do this(commented below),redundent work
                # address.Owner = request.user.Customer
                # address.save(update_fields=['Owner'])
                messages.success(request,'Shipping address selected successfully for this order!')
                return HttpResponseRedirect(reverse('select_payment_gateway'))
            else:
                allAddress = ShippingAddress.objects.filter(Owner_id=request.user.Customer_id)
                if allAddress.exists():
                    return render(request,'store,components/oreder/selectAddress.html',{
                        'allAddress' : allAddress,
                    })
                else:
                    messages.warning('request',"You currently don't have any address please Add One!")
                    return HttpResponseRedirect(reverse('orderpage'))
    else:
        return HttpResponseRedirect(reverse('register'))

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
                # if in transition proceess will vary
                if 'in_transition' in request.session:
                    # request.session['register_complete'] = True
                    return HttpResponseRedirect(reverse('orderpage'))
                else:
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
            if 'in_transition' in request.session:
                print(f'------register success REDIRECTING-----')
                request.session['register_complete'] = True
                return HttpResponseRedirect(reverse('orderpage'))
            else:
                return HttpResponseRedirect(reverse('cartpage'))
            # new_user.save() #signal will automatically create and attach customer instance
            # # new_user.refresh_from_db() #now will be able to acess Customer profile
        else:
            return render(request,'store/components/user/register.html',{ 'form' : formData })
        print('got POST')
        print(request.POST)
    else:
        if 'in_transition' in request.GET:
            # ideally i should check IF any items also exist in cart
            request.session['in_transition'] = True
            request.session['register_complete'] = False
            messages.info(request,'Please register to place order, if already registerd <a href="/handle_login/" class="tw-text-blue-500 tw-font-medium tw-underline">CLICK HERE</a>')
            return render(request,'store/components/user/register.html',{ 'form' : CustomUserCreationForm() })

def handle_cart_convert(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # NO NEED FOR DE-SEREALIZATION AS SESSION ALWYS SEREAILISES
            # cartData = loads(request.body)
            # print(cartData)
            request.session['cart'] = loads(request.body)
            print(f'-------Recived cart-------')
            return HttpResponse(status=200)
        else:
            return HttpResponse('Forbidden',status=403)


def print_session(request):
    if 'clear' in request.GET:
        if request.GET['clear'] == 'viewed':
            request.session['viewed'] = []
        else:
            pass
    print(request.session.keys())
    print(request.session.items())
    # print(request.session['varstr'])
    # print(request.session['prodstr'])
    # print(request.session['items'])
    # print(request.session['prodList'])
    return HttpResponse(status=200)

@csrf_exempt
def paytm_response(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, settings.PAYTM_MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            order = Order.objects.get(pk=response_dict['ORDERID'])
            order.Status = '1'
            order.save(update_fields=['Status'])
            messages.success(request,f'Your order amount is recived, your order id is : {response_dict["ORDERID"]}, use this for tracking!')
            del request.session['this_order_shipadd_id_willbe']
            print('order successful')
        else:
            order = Order.objects.get(pk=response_dict['ORDERID'])
            order.Status = '-1'
            order.save(update_fields=['Status'])
            messages.error(request,'An Error occured, order not completed')
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})