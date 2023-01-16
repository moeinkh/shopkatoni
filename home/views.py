from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from product.models import Category, Product, Comment, Images, Variants, Brand, IpAddress, Color, Slider
from user.models import User
from .models import Setting, Article, Contact
from .forms import ContactForm
from django.core.paginator import Paginator, EmptyPage

# search_form
from product.filter import ProductFilter, VariantFilter
# Create your views here.


def home(request):
    context = {
        'category': Category.objects.all(),
        'product': Product.objects.all(),
        'brand': Brand.objects.all(),
        'news': Product.objects.all().order_by('-id')[:5],
        'discount': Product.objects.filter(discount_price=True),
        'articles': Article.objects.all(),
        'sliders': Slider.objects.all().order_by('-id')[:4]
    }
    return render(request, 'home/home.html', context)


def about(request):
    try: 
        setting = get_object_or_404(Setting, pk=1)
        context = {
            'setting': setting
        }
        return render(request, 'home/about.html', context)
    except:
        return redirect('home:home')

def contact_us(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('home:contact')
    else:
        contact_form = ContactForm()
    return render(request, 'home/contact.html', {
        'contact_form': contact_form
    })


def articles(request):
    context = {
        'articles': Article.objects.all(),
    }
    return render(request, 'home/articles.html', context)


def details_articles(request, id):
    context = {
        'articles': get_object_or_404(Article, pk=id)
    }
    return render(request, 'home/details_articles.html', context)


def details(request, id, slug):
    query = request.GET.get('q')
    product = get_object_or_404(Product, id=id, slug=slug)

    for ip_address in IpAddress.objects.all():
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)

    context = {
        'product': product,
        'product_related': Product.objects.filter(brand__name=product.brand.name, gender=product.gender).exclude(id=id)[:4],
        'images': Images.objects.filter(product_id=id),
        'comments': Comment.objects.filter(product_id=id, active=True).order_by('-id'),
    }
    
    if product.variant != 'None':
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.filter(product_id=id).values('size_id', 'size__name').distinct()
            # query += variant.title + ' size:' + str(variant.size) + ' color:' + variant.color

        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.filter(product_id=id).values('size_id', 'size__name').distinct()
            variant = Variants.objects.get(id=variants[0].id)
        context.update({
            'sizes': sizes,
            'colors': colors,
            'variant': variant,
            'query': query
        })
    return render(request, 'home/product.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('home/color_list.html', context, request=request)}
        return JsonResponse(data)
    return JsonResponse(data)


def katoni(request, brand_slug=None, category_slug=None):
    category = None
    categories = Category.objects.all()
    brand = None
    brands = Brand.objects.all()
    katonis = Product.objects.all().order_by('-id').order_by('status')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        katonis = katonis.filter(category=category)
    elif brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        katonis = katonis.filter(brand=brand)



    search_brand = request.GET.get('search_brand')
    search = request.GET.get('search')
    if search_brand:
        katonis = Product.objects.filter(Q(brand__name__in=request.GET.getlist('search_brand'))
                                           | Q(status=True)
                                           | Q(name__icontains=search)).distinct().order_by('-id').order_by('status')

    product_filter = ProductFilter(request.GET, queryset=katonis)
    variant_filter = VariantFilter(request.GET, queryset=Variants.objects.all())
    katonis = product_filter.qs
    pagination = Paginator(katonis, 20)
    page_number = request.GET.get('page')
    pages = pagination.get_page(page_number)

    context = {
        'category': category,
        'katonis': katonis,
        'pages': pages,
        'pagination': pagination,
        'product_filter': product_filter,
        'variant_filter': variant_filter,
        'search_brand': search_brand,
        'brands': Brand.objects.all(),
        'colors': Color.objects.all(),
        'pro_count': Product.objects.all().count(),
    }
    return render(request, 'home/katonis.html', context)


def for_men(request):
    category = Category.objects.all()
    search_bar = request.GET.get('search_bar')
    if search_bar:
        for_men = Product.objects.filter(Q(name__icontains=search_bar)
                                         | Q(brand__name__icontains=search_bar)
                                         | Q(orderproduct__variant__size__name=search_bar)
                                         | Q(orderproduct__variant__color__name=search_bar)
                                         | Q(status=True)
                                         & Q(gender=1)).distinct().order_by('-id').order_by('status')
    else:
        for_men = Product.objects.filter(gender=1).order_by('-id').order_by('status')
    product_filter = ProductFilter(request.GET, queryset=for_men)

    variant_filter = VariantFilter(request.GET, queryset=Variants.objects.all())

    for_men = product_filter.qs
    pagination = Paginator(for_men, 20)
    page_number = request.GET.get('page')
    pages = pagination.get_page(page_number)
    context = {
        'category': category,
        'pages': pages,
        'pagination': pagination,
        'product_filter': product_filter,
        'variant_filter': variant_filter,
        'search_bar': search_bar,
        'brands': Brand.objects.all(),
        'colors': Color.objects.all(),
        'pro_count': Product.objects.filter(gender=1).count(),
    }
    return render(request, 'home/for_men.html', context)


def feminine(request):
    category = Category.objects.all()
    search_bar = request.GET.get('search_bar')
    if search_bar:
        feminine = Product.objects.filter(Q(name__icontains=search_bar)
                                          | Q(brand__name__icontains=search_bar)
                                          | Q(orderproduct__variant__size__name=search_bar)
                                          | Q(orderproduct__variant__color__name=search_bar)
                                          | Q(status=True)
                                          & Q(gender=2)).distinct().order_by('-id').order_by('status')
    else:
        feminine = Product.objects.filter(gender=2).order_by('-id').order_by('status')
    product_filter = ProductFilter(request.GET, queryset=feminine)
    variant_filter = VariantFilter(request.GET, queryset=Variants.objects.all())

    feminine = product_filter.qs
    pagination = Paginator(feminine, 20)
    page_number = request.GET.get('page')
    pages = pagination.get_page(page_number)
    context = {
        'category': category,
        'pages': pages,
        'pagination': pagination,
        'product_filter': product_filter,
        'variant_filter': variant_filter,
        'search_bar': search_bar,
        'brands': Brand.objects.all(),
        'colors': Color.objects.all(),
        'pro_count': Product.objects.filter(gender=2).count(),
    }
    return render(request, 'home/feminine.html', context)


def both(request):
    category = Category.objects.all()
    search_bar = request.GET.get('search_bar')
    if search_bar:
        both = Product.objects.filter(Q(name__icontains=search_bar)
                                          | Q(brand__name__icontains=search_bar)
                                          | Q(orderproduct__variant__size__name=search_bar)
                                          | Q(orderproduct__variant__color__name=search_bar)
                                          | Q(status=True)
                                          & Q(gender=2)).distinct().order_by('-id').order_by('status')
    else:
        both= Product.objects.filter(gender=3).order_by('-id').order_by('status')
    product_filter = ProductFilter(request.GET, queryset=both)
    variant_filter = VariantFilter(request.GET, queryset=Variants.objects.all())

    both = product_filter.qs
    pagination = Paginator(both, 20)
    page_number = request.GET.get('page')
    pages = pagination.get_page(page_number)
    context = {
        'category': category,
        'pages': pages,
        'pagination': pagination,
        'product_filter': product_filter,
        'variant_filter': variant_filter,
        'search_bar': search_bar,
        'brands': Brand.objects.all(),
        'colors': Color.objects.all(),
        'pro_count': Product.objects.filter(gender=3).count(),
    }
    return render(request, 'home/both.html', context)


def discounts(request):
    category = Category.objects.all()
    search_bar = request.GET.get('search_bar')
    if search_bar:
        discounts = Product.objects.filter(Q(name__icontains=search_bar)
                                           | Q(brand__name__icontains=search_bar)
                                           | Q(orderproduct__variant__size__name=search_bar)
                                           | Q(orderproduct__variant__color__name=search_bar)
                                           | Q(status=True)
                                           & Q(discount_price=True)).distinct().order_by('-id').order_by('status')
    else:
        discounts = Product.objects.filter(discount_price=True).order_by('-id').order_by('status')

    product_filter = ProductFilter(request.GET, queryset=discounts)

    variant_filter = VariantFilter(request.GET, queryset=Variants.objects.all())

    for_men = product_filter.qs
    pagination = Paginator(for_men, 20)
    page_number = request.GET.get('page')
    pages = pagination.get_page(page_number)
    context = {
        'category': category,
        'pages': pages,
        'pagination': pagination,
        'product_filter': product_filter,
        'variant_filter': variant_filter,
        'search_bar': search_bar,
        'brands': Brand.objects.all(),
        'colors': Color.objects.all(),
    }
    return render(request, 'home/discounts.html',context)

