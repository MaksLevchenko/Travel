from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from taggit.models import Tag

from .forms import SigUpForm, SignInForm, FeedBackForm, CommentForm
from .models import Post, Comment


class MaineView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'home.html',
            context={
                'page_obj': page_obj
            }
        )


class PostDetailView(View):
    """Пост"""
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:5]
        comment_form = CommentForm()
        return render(request, 'post_detail.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_posts': last_posts,
            'comment_form': comment_form
        })

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            post = get_object_or_404(Post, url=slug)
            comment = Comment.objects.create(post=post, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'post_detail.html', context={
            'comment_form': comment_form
        })


class SignUpView(View):
    """Авторизация"""
    def get(self, request, *args, **kwargs):
        form = SigUpForm()
        return render(request, 'signup.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SigUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'signup.html', context={
            'form': form
        })


class SignInView(View):
    """Регистрация"""
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'signin.html', context={
            'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'signin.html', context={
            'form': form
        })


class FeedBackView(View):
    """Обратная связь"""
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'contact.html', context={
            'form': form,
            'title': 'Написать мне'
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}', message, from_email, ['levchenkomaksmsk@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'contact.html', context={
            'form': form,
        })


class SuccessView(View):
    """Благодарность"""
    def get(self, request, *args, **kwargs):
        return render(request, 'success.html', context={
            'title': 'Спасибо'
        })


class SearchResultsView(View):
    """Поиск"""
    def get(self, request, *args, **kwargs):
        qwery = self.request.GET.get('q')
        results = ''
        if qwery:
            results = Post.objects.filter(
                Q(h1__icontains=qwery) | Q(content__icontains=qwery)
            )
        return render(request, 'search.html', context={
            'title': 'Поиск',
            'results': results,
            'count': len(results)
        })


class TagView(View):
    """Тэг"""
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'tag.html', context={
            'title': f'#ТЕГ {tag}',
            'posts': posts,
            'common_tags': common_tags
        })
