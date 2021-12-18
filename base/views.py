from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, DetailView
from django.http import HttpResponse

from .forms import InputForm, ModularLocalFormset, LocalizationFormset
from .reader import clean_data
from .models import Documentation
from .supervisors.localization import SupervisorLocalizado
from .supervisors.supervisor import Supervisor, Plant
from .supervisors.modular_local import ModularLocal
from .language.c import C, Arduino


def file_request(request):
    response = HttpResponse(request.session['code'], content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="foo.txt"'
    return response


class HomeView(TemplateView):
    template_name = 'home.html'


class DocumentationListView(ListView):
    model = Documentation
    template_name = 'documentation.html'


class DocumentationView(DetailView):
    model = Documentation
    template_name = 'documentation_detail.html'


class ModularLocalView(FormView):
    template_name = 'modular_local.html'
    form_class = InputForm
    success_url = reverse_lazy('base:home')

    def get_context_data(self, **kwargs):
        context = super(ModularLocalView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            context['formset'] = ModularLocalFormset(self.request.POST, self.request.FILES)
        else:
            context['formset'] = ModularLocalFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset = formset.cleaned_data
            if form.cleaned_data['linguagem'] == "C":
                sup = ModularLocal(C())
            else:
                sup = ModularLocal(Arduino())
            for i in formset:
                data = clean_data(i['automato'])
                if i['type'] == 'S':
                    automato = Supervisor(data)
                else:
                    automato = Plant(data)
                sup.set_data(automato)
            self.request.session['code'] = sup.createcode()
            return redirect('base:file')
        return super().form_valid(form)


class LocalizationView(FormView):
    template_name = 'localization.html'
    form_class = InputForm

    def get_context_data(self, **kwargs):
        context = super(LocalizationView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            context['formset'] = LocalizationFormset(self.request.POST, self.request.FILES)
        else:
            context['formset'] = LocalizationFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset = formset.cleaned_data
            self.request.session['code'] = ""
            for i in formset:
                if form.cleaned_data['linguagem'] == "C":
                    sup = SupervisorLocalizado(C())
                else:
                    sup = SupervisorLocalizado(Arduino())
                p = Plant(clean_data(i['plant']))
                s = Supervisor(clean_data(i['supervisor']))
                sup.set_data(p)
                sup.set_data(s)
                self.request.session['code'] += sup.createcode()
            return redirect('base:file')
        return super().form_valid(form)
