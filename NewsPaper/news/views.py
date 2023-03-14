from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from django.shortcuts import render
from django.views import View # импортируем простую вьюшку
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно 
from .filters import *
from .forms import *
from .models import *

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

class NewsListFilt(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'
    paginate_by = 10
    
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'news/newsDetail.html'
    context_object_name = 'news'


class Posts (View):
    def get(self, request):
        posts = Post.objects.all()
        p = Paginator(posts, 1)
        posts = p.get_page(request.GET.get('page', 1)) 

        data = {
            'posts': posts,
        }
        return render(request, 'news/news.html', data)
    

class PostCreateView(CreateView):
    template_name = 'news/add.html'
    form_class = NewsForm

class PostUpdateView(UpdateView):
    template_name = 'news/add.html'
    form_class = NewsForm
 
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'