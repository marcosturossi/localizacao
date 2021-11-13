from django import forms
from django.forms import formset_factory

LANGUAGE = (
    ('C', 'C'),
    ('A', 'Arduino'),
    ('P', 'Python'),
)

architecture = (
    ('L', 'Localizacao'),
    ('ML', 'Modular Local')
)


class InputForm(forms.Form):
    linguagem = forms.ChoiceField(choices=LANGUAGE)
    arquitetura = forms.ChoiceField(choices=architecture)


class AutomataForm(forms.Form):
    planta = forms.FileField()
    supervisor = forms.FileField()
    eventos_controlaveis = forms.CharField(required=False, label='Eventos Controlávels',
                                           widget=forms.TextInput(attrs={'placeholder': 'exemplo - e1,e3,e5...'}))


AutomataFormset = formset_factory(AutomataForm)
