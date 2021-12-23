from django.forms import ModelForm
from .models import Comentario

class FormComentario(ModelForm):
    # validações
    def clean(self):
        data = self.cleaned_data

        nome = data.get('nome')
        email = data.get('email')
        comentario = data.get('comentario')

        if len(nome):
            self.add_error(
                'nome', 'Nome precisa ter no mínimo 5 caracteres.'
            )

        if not comentario:
            self.add_error(
                'comentario', 'Adicione um comentário.'
            )

    class Meta:
        model = Comentario
        fields = ('nome', 'email', 'comentario')