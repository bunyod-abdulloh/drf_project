from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Books
from .serializers import BooksSerializers


# class View ommabop, ko'pchilik dasturchilar shundan foydalanishadi
# class BookListAPIView(generics.ListAPIView):
#     """
#     DBdagi barcha ma'lumotlarni tanlagan columnlaridagi qiymatlarini ko'rsatadi
#     """
#     queryset = Books.objects.all()
#     serializer_class = BooksSerializers


class BookListApiView(APIView):

    def get(self, request):
        books = Books.objects.all()
        serializer_data = BooksSerializers(books, many=True).data
        data = {
            "status": f"Returned {len(books)} books",
            "books": serializer_data
        }

        return Response(data=data)


# class BookDetailApiView(generics.RetrieveAPIView):
#     """
#     Bitta kitob ma'lumotlarini qaytaruvchi class
#     """
#     queryset = Books.objects.all()
#     serializer_class = BooksSerializers

class BookDetailApiView(APIView):

    def get(self, request, pk):
        try:
            book = Books.objects.get(id=pk)
            serializer_data = BooksSerializers(book).data
            data = {
                'status': True,
                'book': serializer_data
            }
            return Response(data=data)
        except Exception:
            data = {
                'status': False,
                'message': 'Kitob topilmadi!'
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


# class BookDeleteApiView(generics.DestroyAPIView):
#     queryset = Books.objects.all()
#     serializer_class = BooksSerializers

class BookDeleteApiView(APIView):

    def delete(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        book.delete()
        data = {
            'status': True,
            'message': 'Kitob o\'chirildi!'
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
    # try:
    #     book = Books.objects.filter(id=pk)
    #     book.delete()
    #     data = {
    #         'status': True,
    #         'message': 'Kitob o\'chirildi!'
    #     }
    #     return Response(data=data, status=status.HTTP_200_OK)
    # except Exception:
    #     data = {
    #         'status': False,
    #         'message': 'Kitob topilmadi!'
    #     }
    #     return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


# class BookUpdateApiView(generics.UpdateAPIView):
#     queryset = Books.objects.all()
#     serializer_class = BooksSerializers
#     http_method_names = ['put', 'patch']

class BookUpdateApiView(APIView):

    def put(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        data = request.data
        serializer = BooksSerializers(instance=book, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            book_saved = serializer.save()
        return Response(data={
            'status': True, 'message': f'Ma\'lumotlar o\'zgartirildi!\nKitob: {data.get("subtitle")}'
        }, )


class BookCreateApiView(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "status": True,
            "book": serializer.data
        }, status=status.HTTP_201_CREATED)


class BooksListCreateView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers


# class BookCreateApiView(APIView):
#
#     def post(self, request):
#         serializer = BooksSerializers(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             data = {
#                 "status": True,
#                 "book": serializer.data
#             }
#         return Response(data=data, status=status.HTTP_201_CREATED)
        # else:
        #     data = {
        #         "status": False,
        #         "errors": serializer.errors
        #     }
        #     return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class BooksUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers


class BookViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers

# function viewni hozir ko'pchilik ishlatmaydi
@api_view(['GET'])
def book_list_view(request, *args, **kwargs):
    books = Books.objects.all()
    serializer = BooksSerializers(books, many=True)
    return Response(serializer.data)
