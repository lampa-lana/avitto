from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
from .models import Post, Comment


class PostForm(forms.ModelForm):
    max_size_img = 5

    class Meta:
        model = Post
        fields = ['post_name', 'description',
                  'image', 'price', 'category', 'draft']
        widgets = {
            'post_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Продам что-нибудь'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Подробнее, о том что продаю'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', }),
            'price': forms.NumberInput(attrs={'class': 'form-control', }),


        }

    def clean_post_name(self):
        post_name = self.cleaned_data.get('post_name')
        if len(post_name) < 6:
            raise ValidationError('Наименование слишком короткое!')
        else:
            return post_name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 6:
            raise ValidationError('Описание товара слишком короткое!')
        else:
            return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > self.max_size_img*1024*1024:
                raise ValidationError(
                    'Файл должен быть не больше {} мб'.format(self.max_size_img))
            return image
        else:
            raise ValidationError('Не удалось прочитать файл')


class EmailPostForm(forms.Form):
    subject = forms.CharField(label='Тема', max_length=50)
    from_email = forms.EmailField(label='Email отправителя',)
    to = forms.EmailField(label='Email получателя',)
    message = forms.CharField(widget=forms.Textarea,
                              required=False, label='Комментарии',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст комментария'})
        }

#
# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label='Фотограции Товара')
#
#     class Meta:
#         model = Image
#         fields = ('image', )
