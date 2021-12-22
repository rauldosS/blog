from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post

# Create your views here.
class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

class PostBusca(PostIndex):
    pass

class PostCategoria(PostIndex):
    pass

class PostDetalhes(UpdateView):
    pass