from django.contrib import admin
from .models import Comentario

# Register your models here.
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'comentario', 'post', 'usuario', 'data', 'publicado')
    list_display_links = ('id', 'nome')
    list_editable = ('publicado',)

admin.site.register(Comentario, ComentarioAdmin)