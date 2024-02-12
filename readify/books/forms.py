from django import forms

from .models import Comment, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'score',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class SearchForm(forms.Form):
    search = forms.CharField(label='Введите поисковый запрос',
                             help_text=('Для выполнения поиска введите \
                                        ключевые слова из названия книги,\
                                        из её описания, или автора книги,\
                                        либо жанр книг (для отображения всех \
                                        книг выбранного жанра)'),
                             max_length=50)


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)
