from .models import Book, BookRead, BookToRead


class BookRecommendationService:
    @staticmethod
    def get_recommendations_for_user(user_id):
        books_read = BookRead.objects.filter(
            user_id=user_id).values_list('book', flat=True)
        books_to_read = BookToRead.objects.filter(
            user_id=user_id).values_list('book', flat=True)
        genres = Book.objects.filter(
            id__in=books_read).values_list('genre', flat=True).distinct()
        authors = Book.objects.filter(
            id__in=books_read).values_list('author', flat=True).distinct()
        books = Book.objects.exclude(
            id__in=books_read).exclude(id__in=books_to_read)
        # books_with_rating = Book.objects.annotate(rating=Avg('reviews__score')).filter(rating__gte=6)
        genre_recommendations = books.filter(genre__in=genres)
        author_recommendations = books.filter(author__in=authors)
        recommendations = genre_recommendations & author_recommendations
        return recommendations
