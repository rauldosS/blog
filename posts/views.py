from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario

# Create your views here.
class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(publicado=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado=True, then=1)
                )
            )
        )

        return qs

class PostBusca(PostIndex):
    template_name = 'posts/index.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        termo = self.request.GET.get('termo')

        if termo:
            qs = qs.filter(
                Q(titulo__icontains=termo) |
                Q(autor__first_name__iexact=termo) |
                Q(conteudo__icontains=termo) |
                Q(excerto__icontains=termo) |
                Q(categoria__nome__iexact=termo)
            )

        return qs

class PostCategoria(PostIndex):
    template_name = 'posts/categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()
        
        categoria = self.kwargs.get('categoria', None)

        if categoria:
            qs = qs.filter(categoria__nome__iexact=categoria)

        return qs

class PostDetalhes(UpdateView):
    template_name = 'posts/post.html'
    model = Post

    form_class = FormComentario
    context_object_name = 'post'