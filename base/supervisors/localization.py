from .supervisor import Supervisor


class SupervisorLocalizado(Supervisor):

    def non_plant_event(self):
        """Encontra os eventos não controláveis devido a localização"""
        eventos = set()
        if self.supervisor_events is set():
            self.get_events()
        for i in self.supervisor_events:
            if i not in self.plant_events:
                eventos.add(i)
        return eventos

    def set_transitions(self):
        super().set_transitions()
        non_plant_events = self.non_plant_event()
        k = []
        for i in self.controlable:
            for j in self.controlable[i]:
                if j[1] in non_plant_events:
                    k.append(j)
        for i in self.controlable:
            for n in k:
                if n in self.controlable[i]:
                    self.controlable[i].remove(n)
            self.non_controlable[i] += k

    def set_pin(self):
        """Set se os pinos sao entrada ou saida, de acordo com a localização"""
        code = "\n\n"
        inp = "INPUT"
        out = 'OUTPUT'
        for i in sorted(self.all_events):
            if int(i) % 2 == 0:
                code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", inp], ident=1)
            elif int(i) % 2 != 0 and i in self.non_plant_event():
                code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", out], ident=1)
            else:
                code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", out], ident=1)
        return code
