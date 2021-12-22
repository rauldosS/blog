from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Post(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Título')
    autor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.DateTimeField(default=datetime.now())
    conteudo = models.TextField(verbose_name='Conteúdo')
    excerto = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, blank=True, null=True)
    imagem = models.ImageField(upload_to='posts/images/%Y/%m/%d')
    publicado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titulo