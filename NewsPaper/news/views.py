from django.views.generic import ListView, DetailView

from .models import *

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
        #Сделайте новую страничку с адресом /news/, на которой должен выводиться список всех новостей.
        #Сделайте отдельную страничку для конкретной новости по адресу /news/<id новости>.
       # Все странички должны быть частью основного шаблона default.html.
