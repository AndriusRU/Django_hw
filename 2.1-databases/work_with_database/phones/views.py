from django.shortcuts import render, redirect
#from phones.models import Phone

from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sortType = request.GET.get('sort', "")
    if sortType == 'name':
        context = {'phones': Phone.objects.order_by(sortType)}
    elif sortType == 'min_price':
        context = {'phones': Phone.objects.order_by('price')}
    elif sortType == 'max_price':
        context = {'phones': Phone.objects.order_by('-price')}
    else:
        context = {'phones': Phone.objects.all()}

    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {'phone': Phone.objects.get(slug=slug)}
    print(context)
    return render(request, template, context)
