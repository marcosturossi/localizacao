from .supervisor import Supervisor


class SupervisorLocalizado(Supervisor):
    def non_plant_event(self):
        """Encontra os eventos não controláveis devido a localização"""
        eventos = set()
        if self.plant_events is None and self.supervisor_events is None:
            self.get_events()
        for i in self.supervisor_events:
            if i not in self.plant_events and int(i) % 2 != 0:
                eventos.add(i)
        return sorted(eventos)

    def set_events(self):
        # TODO criar self.controlable_events... etc
        # TODO refatorar os valores
        pass

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
