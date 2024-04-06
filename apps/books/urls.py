from django.urls import path

from apps.books.views import BookListView, BookDetailView, AddReviewView, AddBookView

app_name = "books"

urlpatterns = [
    path('', BookListView.as_view(), name="book-list"),
    path('add_book/', AddBookView.as_view(), name="add-book"),
    path('<slug:slug>/', BookDetailView.as_view(), name="book-detail"),
    path('<int:pk>', AddReviewView.as_view(), name="add-review")

]
