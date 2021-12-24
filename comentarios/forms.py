from django.forms import ModelForm
from .models import Comentario
import requests

class FormComentario(ModelForm):
    # validações
    def clean(self):
        raw_data = self.data
        recaptcha_response = raw_data.get('g-recaptcha-response')
        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': '6Lfds8QdAAAAAOl-JT_xnUm8euIQ5W4WcCqCA9rs',
                'response': recaptcha_response
            }
        )
        recaptcha_result = recaptcha_request.json()

        print(recaptcha_result)
        print(recaptcha_result.get('success'))

        if not recaptcha_result.get('success'):
            self.add_error(
                'comentario',
                'Desculpe Mr. Robot, ocorreu um erro.'
            )

        cleaned_data = self.cleaned_data
        nome = cleaned_data.get('nome')
        email = cleaned_data.get('email')
        comentario = cleaned_data.get('comentario')

        if len(nome) < 5:
            self.add_error(
                'nome',
                'Nome precisa ter mais que 5 caracteres.'
            )

    class Meta:
        model = Comentario
        fields = ('nome', 'email', 'comentario')