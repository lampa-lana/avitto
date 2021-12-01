from django.http.response import Http404, HttpResponseRedirect
from django.utils import timezone
from django.db.models.aggregates import Sum
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory, modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Context, context, loader
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView, View
from .models import Post, Category, Profile, Comment
from .forms import PostForm, EmailPostForm, CommentForm
from django.forms import modelformset_factory
from avitto.settings import FROM_EMAIL, EMAIL_ADMIN


# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = 'core/index.html'
    context_object_name = 'posts'
    extra_context = {'page_title': 'Главная'}
    queryset = model.objects.all().filter(
        draft=False).order_by('-date_edit')[:12]
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class AllPostView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'core/all_posts.html'
    extra_context = {'page_title': 'Все объявления'}
    queryset = model.objects.all().order_by(
        '-date_edit').filter(draft=False)
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


# def all_posts(request):
#     # все посты
#     posts = Post.objects.all().order_by('category')
#     context = {
#         'posts': posts,
#         'title': "Все объявления"}
#     return render(request, template_name='core/all_posts.html', context=context)

class PostDetailView(DetailView):
    model = Post
    comment_form = CommentForm
    pk_url_kwarg = "post_id"
    template_name = 'core/post_detail.html'
    extra_context = {'page_title': 'Подробнее об объявлении'}

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        # context['images'] = Image.objects.filter(post_id=post_id)
        # context['images_all'] = Image.objects.all()
        context['posts'] = Post.objects.filter(draft=True)
        context['categories'] = Category.objects.all()
        context['comments'] = Comment.objects.filter(
            post__pk=post_id).order_by('-timestamp')
        context['comment_form'] = None
        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        form = self.comment_form(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.timestamp = timezone.now()
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('core:post_detail', post_id)
        else:
            return render(request=request, template_name=self.template_name, context={'comment_form': form,
                                                                                      'post': post,
                                                                                      'categories': Category.objects.all(),
                                                                                      #   'images': Image.objects.filter(post_id=post_id),

                                                                                      })
# def post_detail(request, post_id):
#     # детали поста
#     post = get_object_or_404(Post, id=post_id)
#     context = {
#         'post': post,
#         'title': ("Подробнее об: {}".format(post.post_name))}
#     return render(request, template_name='core/post_detail.html', context=context)


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'core/post_create.html'
    login_url = '/admin/login'
    extra_context = {'page_title': 'Создать объявление'}

    # def get(self, request,  *args, **kwargs):
    #     ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    #     print('ok1')
    #     if request.method == "GET":
    #         print('ok2')
    #         form = PostForm()
    #         formset = ImageFormSet(queryset=Image.objects.none())
    #         print('ok2-1')
    #         return render(request, self.template_name,  {"form": form, "formset": formset})
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('core:post_detail', kwargs={'post_id': post.id}))
        else:
            return render(request, 'core/post_create.html', {
                'form': form})
    # @ method_decorator(login_required)
    # def post(self, request,  *args, **kwargs):
    #     # form = self.form_class(request.POST, request.FILES)
    #     # if form.is_valid():
    #     #     post = form.save(commit=False)
    #     #     post.author = request.user
    #     #     post.save()
    #     #     return redirect(reverse('core:post_detail', kwargs={'post_id': post.id, }))
    #     # else:
    #     #     return render(request, 'core/post_create.html', {
    #     #         'form': form})
    #     ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    #     if request.method == 'POST':
    #         form = PostForm(request.POST, request.FILES)
    #         formset = ImageFormSet(request.POST, request.FILES,
    #                                queryset=Image.objects.none())
    #         print('ok3')
    #         if form.is_valid() and formset.is_valid():
    #             post = form.save(commit=False)
    #             post.author = request.user
    #             post.save()
    #             print('ok4')
    #             for form_img in formset.cleaned_data:
    #                 print('ok5')
    #                 if form_img:
    #                     print('ok6')
    #                     image = form_img['image']
    #                     photo = Image(post=post, image=image)
    #                     photo.save()
    #                     print('ok6:')
    #             # use django messages framework
    #             messages.success(request,
    #                              "Yeeew, check it out on the home page!")

    #             return redirect(reverse('core:post_detail', kwargs={'post_id': post.id, }))
    #         else:
    #             print('postForm.errors: ', form.errors,
    #                   'formset.errors: ', formset.errors)
    #             print('ok7')
    #     else:
    #         form = PostForm()
    #         formset = ImageFormSet(queryset=Image.objects.none())
    #         print('ok8')
    #     return render(request, 'core/post_create.html',
    #                   {'postForm': form, 'formset': formset})


# def post_create(request):
#     if request.method == 'GET':
#         form = PostForm()
#         return render(request, 'core/post_create.html', {
#             'form': form})
#     elif request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect(reverse('core:post_detail', kwargs={'post_id': post.id}))
#         else:
#             return render(request, 'core/post_create.html', {
#                 'form': form})
        # return HttpResponse('post_create')

class PostDelete(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_delete.html'
    extra_context = {'page_title': 'Удалить объявление'}

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('core:post_delete_success', args=(post_id, ))


class EditView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_edit.html'
    form_class = PostForm
    extra_context = {'page_title': 'Изменить объявление'}

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('core:post_detail', args=(post_id, ))


class CategoriesDetailView(DetailView):
    model = Category
    pk_url_kwarg = "category_id"
    template_name = 'core/cat_detail.html'
    extra_context = {'page_title': 'Об категории'}

    def get(self, request, category_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['posts'] = Post.objects.filter(category_id=category_id)
        context['category'] = Category.objects.get(pk=category_id)
        context['categories'] = Category.objects.all()

        return self.render_to_response(context)


# def category_detail(request, category_id):
#     posts = Post.objects.filter(category_id=category_id)
#     categories = Category.objects.all()
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'posts': posts,
#         'categories': categories,
#         'category': category,
#         'title': "Побробнее о категориях", }
#     return render(request, template_name='core/cat_detail.html', context=context)


class AllCategoryView(ListView):
    model = Category
    template_name = 'core/categories.html'
    context_object_name = 'categories'
    extra_context = {'page_title': 'Категории'}

    def get_queryset(self):
        return self.model.objects.all()


# def category_all(request):
#     categories = Category.objects.all()
#     context = {
#         'categories': categories,
#         'title': "Категории", }
#     return render(request, template_name='core/categories.html', context=context)


# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1> Страница не найдена</h1>')
#


# def post_share(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     sent = False
#     # if request.method == 'GET':
#     #     form = EmailPostForm()
#     if request.method == 'POST':

#         # From was submitted
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = '{}({})рекомендует Вам посмотреть "{}"'.format(cd['subject'],
#                                                                      cd['from_email'],
#                                                                      post.post_name)
#             message = 'Посмотреть"{}" at {} \n\n\' о:{}'.format(post.post_name,
#                                                                 post_url,
#                                                                 cd['subject'],
#                                                                 cd['message'])
#             send_mail(subject, message, cd['from_email'], [cd['to']])
#             sent = True

#     else:
#         form = EmailPostForm()
#     return render(request, 'core/share.html', {'post': post, 'form': form, 'sent': sent})


class PostShare(View):
    model = Post
    form = EmailPostForm()
    queryset = model.objects.all()
    template_name = 'core/share.html'

    def get(self, request, *args, **kwargs):
        context = {
            'post': self.model.objects.all(),
            'form': self.form
        }
        return render(request, 'core/share.html', context)

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        sent = False
        print('ok1')

        if request.method == 'POST':
            print('ok2')

            form = EmailPostForm(request.POST)
            if form.is_valid():
                print('ok3')
                cd = form.cleaned_data
                post_url = request.build_absolute_uri(post.get_absolute_url())
                subject = '{}({})рекомендует Вам посмотреть "{}"'.format(cd['subject'],
                                                                         cd['from_email'],
                                                                         post.post_name)
                message = 'Посмотреть объявление можно "{}" \n\n\' можно по  ссылке {} \n\n\' {}:\n\n\' {}'.format(post.post_name,
                                                                                                                   post_url,
                                                                                                                   cd['subject'],
                                                                                                                   cd['message'],)
                send_mail(subject, message, cd['from_email'], [cd['to']])
                sent = True

        else:
            print('ok4')
            form = EmailPostForm()
        return render(request, 'core/share.html', {'post': post, 'form': form, 'sent': sent})


# def post_create(request, *args, **kwargs):
#     ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
#     print('ok1')

#     if request.method == "GET":

#         print('ok2')
#         form = PostForm()
#         formset = ImageFormSet(queryset=Image.objects.none())
#         print('ok2-1')
#         return render(request, 'core/post_create.html',  {"form": form, "formset": formset})

#     elif request.method == 'POST':

#         form = PostForm(request.POST, request.FILES)
#         formset = ImageFormSet(request.POST, request.FILES,
#                                queryset=Image.objects.none())
#         print('ok3')

#         if form.is_valid() and formset.is_valid():

#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             print('ok4')
#             for form_img in formset.cleaned_data:
#                 print('ok5')
#                 if form_img:
#                     print('ok6')
#                     image = form_img['image']
#                     photo = Image(post=post, image=image)
#                     photo.save()
#                     print('ok6')
#             # use django messages framework
#             messages.success(request,
#                              "Yeeew, check it out on the home page!")

#             return redirect(reverse('core:post_detail', kwargs={'post_id': post.id, }))
#         else:
#             print('postForm.errors: ', form.errors,
#                   'formset.errors: ', formset.errors)
#             print('ok7')
#     else:
#         form = PostForm()
#         formset = ImageFormSet(queryset=Image.objects.none())
#         print('ok8')
#     return render(request, 'core/post_create.html',
#                   {'postForm': form, 'formset': formset})
