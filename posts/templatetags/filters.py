from django import template

register = template.Library()

@register.filter(name='plural_comentarios')
def plural_comentarios(num_comentarios):
    try:
        num_comentarios = int(num_comentarios)

        if num_comentarios == 0:
            return f'Nenhum comentário'
        else:
            return f'{ num_comentarios } comentário{ "s" if num_comentarios > 1 else "" }'
    except:
        return f'{ num_comentarios } comentário(s)'
