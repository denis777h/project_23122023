from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView
)

from .filter import NewsFilter
from .forms import NewsForm
from .models import News


class NewsList(ListView):
    model = News
    ordering = 'name'
    template_name = 'news_press.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterer'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news_press.html'
    context_object_name = 'news'



class NewsCreate(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news_list.html'

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.GET = None

    def news_list(request):
        news_list = News.objects.all()
        paginator = Paginator(news_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'news_press.html', {'page_obj': page_obj})



class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('post_delete',)
    template_name = 'post_delete.html'
    queryset = News.objects.all()
    success_url = reverse_lazy('news')




#s1 = NewsCreate()
#s1.news_list()


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='news')
    if not request.user.groups.filter(name='news').exists():
        authors_group.user_set.add(user)
    return redirect('/')