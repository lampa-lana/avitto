from django.contrib import admin
from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db.models import fields
from django.utils.safestring import mark_safe
from .models import Profile, Post, Category, Comment
from django.utils.text import slugify

# Register your models here.


class ProfileInlineForm(forms.ModelForm):
    class Meta:
        model = Profile

        widgets = {
            'about': forms.Textarea(attrs={'row': 1, 'cols': 50}),
        }
        fields = '__all__'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'foto', 'birth_date',)
    list_display_links = ('user', 'id',)
    search_fields = ('id', 'birth_date')
    list_filter = ('user', 'id', 'birth_date')
    readonly_fields = ['preview', ]
    fields = [('user', 'birth_date'),
              ('about', 'preview', 'foto'), 'post']
    form = ProfileInlineForm

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.foto.url}" style="max-height: 100px;">')

#
# class ImageLine(admin.TabularInline):
#     model = Image


class PostAdmin(admin.ModelAdmin):

    # inlines = [
    #     ImageLine
    # ]

    list_display = ('author', 'post_name', 'date_pub',
                    'price', 'category', 'draft', 'slug')
    list_display_links = ('author',  'category')
    list_editable = ['post_name', 'draft', ]
    actions = ['unpublish', 'publish']
    search_fields = ('post_name', 'author', )
    prepopulated_fields = {'slug': ('post_name',)}
    list_filter = ('category', 'author',  'date_pub', 'price', )
    readonly_fields = ['date_pub', 'date_edit', 'image_url', 'preview', ]
    # fields = ['author', ('post_name',
    #           'category'), ('description', 'price'), ('preview', 'image'), ('date_pub', 'date_edit')]

    fieldsets = [
        ['Основная информация', {'fields': [
            'author',
            ('post_name', 'category', 'slug'), ]}],
        ['Подробнее об объявлении', {'fields': [
            ('description', 'price'),
            ('preview', 'image'), ]}],
        ['Даты публикаций', {'fields': [
            ('date_pub', 'date_edit', 'draft'), ]}],

    ]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image_url}" style="max-height: 200px;">')

    preview.short_description = "Фото"

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description', )
    list_display_links = ('category_name', 'description', )
    search_fields = ('category_name',)
    list_filter = ('category_name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user',  'post')
    list_display_links = ('user', )
    search_fields = ('user',)
    list_filter = ('post',)
    fields = [('user',),
              ('content', 'post'), ]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
# ---------------------------END Profile, Post, Category-----------------------------
admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = ['preview', ]
    fields = [('user', 'birth_date'),
              ('about', 'preview', 'foto'), ]
    form = ProfileInlineForm

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.foto.url}" style="max-height: 200px;">')


class PostInline(admin.StackedInline):
    model = Post
    readonly_fields = ['date_pub', 'date_edit', 'image_url', 'preview', ]

    fieldsets = [
        ['Основная информация', {'fields': [
            'author',
            ('post_name', 'category'), ]}],
        ['Подробнее об объявлении', {'fields': [
            ('description', 'price'),
            ('preview', 'image'), ]}],
        ['Даты публикаций', {'fields': [
            ('date_pub', 'date_edit'), ]}],
    ]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image_url}" style="max-height: 200px;">')


@admin.register(User)
class MyUserAdmin(UserAdmin):
    inlines = [ProfileInline, PostInline]


# ------------------------------ END User+Profile+Post--------------------------------------

# class ImageLine(admin.TabularInline):
#     model = Image
