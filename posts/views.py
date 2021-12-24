from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages
from django.views import View

# Create your views here.
class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('categoria') # otimização https://docs.djangoproject.com/en/4.0/ref/models/querysets/#select-related
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

# class PostDetalhes(View):
#     template_name = 'posts/post.html'

#     def setup(self, request, *args, **kwargs):
#         super().setup(request, *args, **kwargs)

#         pk = self.kwargs.get('pk')
#         post = get_object_or_404(Post, pk=pk, publicado=True)
#         self.contexto = {
#             'post': post,
#             'comentarios': Comentario.objects.filter(post=post, publicado=True),
#             'form': FormComentario(request.POST or None),
#         }

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, self.contexto)

#     def post(self, request, *args, **kwargs):
#         form = self.contexto['form']

#         if not form.is_valid():
#             return render(request, self.template_name, self.contexto)

#         comentario = form.save(commit=False)

#         if request.user.is_authenticated:
#             comentario.usuario = request.user

#         comentario.comentario = self.contexto['post']
#         comentario.save()
#         messages.success(request, 'Seu comentário foi enviado para revisão.')
#         return redirect('post', pk=self.kwargs.get('pk'))

class PostDetalhes(UpdateView):
    template_name = 'posts/post.html'
    model = Post

    form_class = FormComentario
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicado=True, post=post.id)

        contexto['comentarios'] = comentarios

        return contexto

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)

        comentario.post = post
        if self.request.user.is_authenticated:
            comentario.usuario = self.request.user
        
        comentario.save()
        messages.success(self.request, 'Seu comentário foi enviado para revisão.')
        return redirect('post', pk=post.id)