from django.urls import reverse_lazy
from django.views.generic import FormView
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import InputForm, AutomataFormset
from .reader import clean_data
from .supervisors.localization import SupervisorLocalizado
from .supervisors.supervisor import Supervisor
from .language.c import C, Arduino


def file_request(request):
    response = HttpResponse(request.session['code'], content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="foo.txt"'
    return response


class Home(FormView):
    template_name = 'home.html'
    form_class = InputForm
    success_url = reverse_lazy('base:home')

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            context['formset'] = AutomataFormset(self.request.POST, self.request.FILES)
        else:
            context['formset'] = AutomataFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset = formset.cleaned_data
            if form.cleaned_data['arquitetura'] == "ML":
                if form.cleaned_data['linguagem'] == "C":
                    supervisor = Supervisor(C())
                else:
                    supervisor = Supervisor(Arduino())
                for i in formset:
                    data_sup = {'plant': clean_data(i['planta']), 'supervisor': clean_data(i['supervisor'])}
                    supervisor.set_data(data_sup)
                self.request.session['code'] = supervisor.createcode_c()
            else:
                self.request.session['code'] = ""
                for i in formset:
                    data_sup = {'plant': clean_data(i['planta']), 'supervisor': clean_data(i['supervisor'])}
                    if form.cleaned_data['linguagem'] == "C":
                        supervisor = SupervisorLocalizado(C())
                    else:
                        supervisor = SupervisorLocalizado(Arduino())
                    supervisor.set_data(data_sup)
                    self.request.session['code'] += supervisor.createcode_c()
            return redirect('base:file')
        return super().form_valid(form)
