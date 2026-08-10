from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    context = {
        "num_books": Book.objects.count(),
        "num_instances": BookInstance.objects.count(),
        "num_instances_available": BookInstance.objects.filter(status="a").count(),
        "num_authors": Author.objects.count(),
    }
    return render(request, template_name="index.html", context=context)


def authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, per_page=2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        "authors": paged_authors,
    }
    return render(request, template_name="authors.html", context=context)

def author(request, author_pk):
    context = {
        "author": Author.objects.get(pk=author_pk),
    }
    return render(request, template_name="author.html", context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = "book"



