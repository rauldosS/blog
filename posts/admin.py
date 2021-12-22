from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'data', 'publicado')
    list_editable = ('publicado',)
    list_display_links = ('id', 'titulo')
    summernote_fields = ('conteudo',)
    
admin.site.register(Post, PostAdmin)