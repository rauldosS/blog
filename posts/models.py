from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image
from django.conf import settings
import os

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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagem_post:
            self.resize_image(self.imagem_post.name, 800)

    @staticmethod
    def resize_image(img_name, new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size
        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return

        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(
            img_path,
            optimize=True,
            quality=60
        )
        new_img.close()