from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Books


class BooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id', 'title', 'subtitle', 'content', 'author', 'isbn', 'price')

    def validate(self, data):
        title = data.get('title', None)
        author = data.get('author', None)

        # 1. Titleni faqat harflardan iborat ekanligini tekshiradi
        if not title.replace(" ", "").isalpha():
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Sarlavha uchun faqat matnlar kiritilishi lozim!'
                }
            )

        # 2. title == author bo‘lishi mumkin emas
        if title.strip().lower() == author.strip().lower():
            raise ValidationError({
                'status': False,
                'message': 'Sarlavha va muallif bir xil bo‘lishi mumkin emas!'
            })

        # 3. Kiritilgan ma'lumotni dbda tekshirish
        if Books.objects.filter(title=title, author=author).exists():
            raise ValidationError({
                'status': False,
                'message': 'Kiritilgan ma\'lumotlar ma\'lumotlar omborida mavjud!'
            })

        return data

    def validate_price(self, price):
        if price < 0 or price > 999999999:
            raise ValidationError({
                'status': False,
                'message': 'Narx noto\'g\'ri kiritilgan!'
            })

# class BooksSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     subtitle = serializers.CharField(max_length=200)
#     content = serializers.TextField()
#     author = serializers.CharField(max_length=100)
#     isbn = serializers.CharField(max_length=13)
#     price = serializers.DecimalField(max_digits=30, decimal_places=2)
