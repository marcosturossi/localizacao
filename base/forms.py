from django import forms
from django.forms import formset_factory

LANGUAGE = (
    ('C', 'C'),
    ('A', 'Arduino'),
    ('P', 'Python'),
)

ORIGEM = (
    ('P', 'Planta'),
    ('S', 'Supervisor'),
)


class InputForm(forms.Form):
    linguagem = forms.ChoiceField(choices=LANGUAGE, widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))


class ModularLocalForm(forms.Form):
    automato = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control form-control-sm'}))
    type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select form-select-sm'}), choices=ORIGEM)


class LocalizationForm(forms.Form):
    plant = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control form-control-sm'}))
    supervisor = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control form-control-sm'}))


ModularLocalFormset = formset_factory(ModularLocalForm, extra=2)

LocalizationFormset = formset_factory(LocalizationForm)
