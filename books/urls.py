from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BookListApiView, BookDetailApiView, BookUpdateApiView, BookDeleteApiView, \
    BooksListCreateView, BooksUpdateDestroyApiView, BookCreateApiView, BookViewSet

router = SimpleRouter()
router.register(prefix='books', viewset=BookViewSet, basename='books')


urlpatterns = [
    # path('books/', BookListApiView.as_view(), ),
    # path('books/list-create/', BooksListCreateView.as_view(), ),
    # path('books/<int:pk>/update-destroy/', BooksUpdateDestroyApiView.as_view(), ),
    # path('books/create/', BookCreateApiView.as_view(), ),
    # path('books/<int:pk>/', BookDetailApiView.as_view(), ),
    # path('books/<int:pk>/update/', BookUpdateApiView.as_view(), ),
    # path('books/<int:pk>/delete/', BookDeleteApiView.as_view(), ),
]

urlpatterns = urlpatterns + router.urls
