from django import forms
from .models import Cachorro, Foto

class CachorroForm(forms.ModelForm):
    class Meta:
        model = Cachorro
        fields = ['nome', 'data_nascimento', 'peso', 'altura']

class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['imagem']





# from django import forms
# from .models import Cachorro


# class cachorroForm(forms.ModelForm):
#     class Meta:
#         model = Cachorro
#         fields = ['nome', 'data_nascimento', 'peso', 'altura', 'foto']
#         widgets = {
#             'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
#         }
