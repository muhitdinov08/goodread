from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.books.forms import AddBookReviewForm, AddBookForm
from apps.books.models import Book, BookReview
from apps.users import User


class BookListView(View):
    def get(self, request):
        queryset = Book.objects.all()
        param = request.GET.get("q", None)

        if param is not None:
            queryset = queryset.filter(title__icontains=param)
        context = {
            "books": queryset,
            "param": param
        }
        return render(request, "books/book-list.html", context=context)


class BookDetailView(View):
    def get(self, request, slug):
        book = Book.objects.get(slug=slug)
        form = AddBookReviewForm()
        context = {
            "book": book,
            "form": form
        }
        return render(request, "books/book-detail.html", context=context)


class AddReviewView(View):
    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        user = User.objects.get(username=request.user.username)
        form = AddBookReviewForm(request.POST)
        if form.is_valid():
            BookReview.objects.create(
                user=user,
                book=book,
                body=form.cleaned_data.get("body"),
                rating=form.cleaned_data.get("rating")
            )
            return redirect(reverse("books:book-detail", kwargs={"slug": book.slug}))
        else:
            context = {
                "book": book,
                "form": form
            }
            return render(request, "books/book-detail.html", context=context)


class AddBookView(View):
    def post(self, request):
        form = AddBookForm(data=request.POST)
        if form.is_valid():
            queryset = Book.objects.all()
            param = request.GET.get("q", None)

            if param is not None:
                queryset = queryset.filter(title__icontains=param)
            context = {
                "books": queryset,
                "param": param
            }
            form.save()
            messages.success(request, "Book successfully added!")
            return redirect(reverse('books:book-list', kwargs={context}))

        else:
            return render(request, "books/add_book.html", context={'form': form})

    def get(self, request):
        form = AddBookForm(data=request.GET)
        return render(request, "books/add_book.html", {'form': form})
