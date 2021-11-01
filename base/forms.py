from django import forms
from django.forms import formset_factory

LANGUAGE = (
    ('C', 'C'),
    ('P', 'Python')
)

architecture = (
    ('L', 'Localizacao'),
    ('ML', 'Modular Local')
)


class InputForm(forms.Form):
    linguagem = forms.ChoiceField(choices=LANGUAGE,
                                  widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    arquitetura = forms.ChoiceField(choices=architecture,
                                    widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))


class AutomataForm(forms.Form):
    planta = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    supervisor = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    eventos_controlaveis = forms.CharField(required=False, label='Eventos Controlávels',
                                           widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                                                         'placeholder': 'exemplo - e1,e3,e5...'}))


AutomataFormset = formset_factory(AutomataForm)
