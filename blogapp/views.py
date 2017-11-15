from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView

from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .models import Article, Comment
from datetime import datetime

from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = "login.html"

class ArticleListView(ListView):
    model = Article
    template_name = "article-list.html"
    ordering = ['title']

    keyword = None # Get keyword in our context if any.

    def get_queryset(self):
        q = super(ArticleListView, self).get_queryset()

        # Search based on tag.
        tag = self.request.GET.get('tag', '')
        if tag:
            q = q.filter(tags__icontains=tag)

        # Search based on title.
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            q = q.filter(title__icontains=self.keyword)

        return q
        # return Article.objects.all().order_by('-title')

    def get_context_data(self, **kwargs):
        """
        - Define extra data for the template.
        """
        c = super(ArticleListView, self).get_context_data(**kwargs)

        # Get the tags from our
        tag_list = []
        for article in Article.objects.all():
            tags = [t.strip() for t in article.tags.split(',')]
            tag_list.extend(tags)

        c['tag_list'] = set(tag_list) # Remove duplicates and put it in the context.
        c['keyword'] = self.keyword

        return c

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article-detail.html"

    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()

        if self.request.method == "post":
            obj.views -= 1
        else:
            obj.views += 1
        obj.save()

        return obj

    def get_context_data(self, **kwargs):
        c = super(ArticleDetailView, self).get_context_data(**kwargs)
        c['comments'] = Comment.objects.filter(article=self.object).order_by('-created')
        return c

    def post(self, request, *args, **kwargs):
        if not self.request.is_authenticated:
            return redirect('/accounts/login/')

        article = self.get_object()

        comment = Comment(comment=self.request.POST.get('comment'), article=article, author=self.request.user, created=datetime.now())
        comment.save()

        article.comments += 1
        article.save()

        return redirect('/article/' + article.id)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'

    model = Article
    fields = ['title', 'content', 'tags']
    template_name = "article-create.html"
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        return super(ArticleCreateView, self).form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'

    model = Article
    fields = ['title', 'content', 'tags']
    template_name = "article-update.html"


    def get_queryset(self):
        q = super(ArticleUpdateView, self).get_queryset()
        return q.filter(author=self.request.user)

    def form_valid(self, form):
        self.form.instance.updated = datetime.now()
        return super(ArticleCreateView, self).form_valid(form)
