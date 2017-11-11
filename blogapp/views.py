from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .models import Articles

# Create your views here.
class SimpleView(TemplateView):
    template_name = "simple.html"

class ArticlesListView(ListView):
    model = Articles
    template_name = "articles.html"
    ordering = ['title']

    keyword = None # Get keyword in our context if any.

    def get_queryset(self):
        q = super(ArticlesListView, self).get_queryset()

        # Search based on tag.
        tag = self.request.GET.get('tag', '')
        if tag:
            q = q.filter(tags__icontains=tag)

        # Search based on title.
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            q = q.filter(title__icontains=self.keyword)

        return q
        # return Articles.objects.all().order_by('-title')

    def get_context_data(self, **kwargs):
        """
        - Define extra data for the template.
        """
        c = super(ArticlesListView, self).get_context_data(**kwargs)

        # Get the tags from our
        tag_list = []
        for article in Articles.objects.all():
            tags = [t.strip() for t in article.tags.split(',')]
            tag_list.extend(tags)

        c['tag_list'] = set(tag_list) # Remove duplicates and put it in the context.
        c['keyword'] = self.keyword
        print self.keyword

        return c
