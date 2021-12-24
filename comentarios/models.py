from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from posts.models import Post

# Create your models here.
class Comentario(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    email = models.EmailField(verbose_name='E-mail')
    comentario = models.TextField(verbose_name='Comentário')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Usuário', blank=True, null=True)
    data = models.DateTimeField(default=datetime.now())
    publicado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome