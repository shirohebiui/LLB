from django.shortcuts import render

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Include string "Book"
    num_include_BOOK_title = Book.objects.filter(title__icontains='book').count()
    num_include_BOOK_genre = Genre.objects.filter(name__icontains='S.F').count()
    num_include_BOOK = num_include_BOOK_genre + num_include_BOOK_title
    #exact - 대소구분O, iexact-대소구분X
    #icontatins - 대소구분X 내용중 일치문자열있으면
    #참고자료 http://pythonstudy.xyz/python/article/310-Django-%EB%AA%A8%EB%8D%B8-API
    #참고자료 https://fabl1106.github.io/django/2019/05/14/Django-21.-%EC%9E%A5%EA%B3%A0-%ED%8E%98%EC%9D%B4%EC%A7%80-%EC%84%9C%EC%B9%AD-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84.html

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1



    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_include_BOOK': num_include_BOOK,
        'num_visits' : num_visits,
    }

    

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic

class BookListView(generic.ListView):
    model = Book


# class BookListView(generic.ListView):
#     model = Book
#     context_object_name = 'my_book_list'   # your own name for the list as a template variable
#     queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
#     template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

#-----------------------------------------------------#
# def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super(BookListView, self).get_context_data(**kwargs)
#         # Create any data and add it to the context
#         context['some_data'] = 'This is just some data'
#         return context

# 1. 슈퍼클래스에서 기존 컨텍스트를 가져온다
# 2. 새로운 컨텍스트 정보를 추가
# 3. 새롭게 업데이트된 컨텍스트 리턴
#-----------------------------------------------------#

class BookDetailView(generic.DetailView):
    model = Book

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')





















