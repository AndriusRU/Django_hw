from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book

def books_view(request):
    template = 'books/books_list.html'
    context = {'books': Book.objects.all()}
    return render(request, template, context)

def books_date_view(request, date):
    template = 'books/books_date.html'
    context = {}
    context['books'] = Book.objects.filter(pub_date=date)

    books = Book.objects.all().order_by('pub_date')
    content = set()
    for elem in books:
        content.add(str(elem.pub_date))
    content = sorted(list(content))
    dict_content = {content[i]: i + 1 for i in range(0, len(content))}


    page_number = dict_content.get(date, 0)
    print(page_number)
    paginator = Paginator(content, 1)
    page = paginator.get_page(page_number)

    context['page'] = page.object_list

    print(page)
    print(page.has_previous())
    print(page.has_next())
    print(date)

    return render(request, template, context)