from .modular_local import ModularLocal


class SupervisorLocalizado(ModularLocal):

    def non_plant_event(self):
        """Encontra os eventos não controláveis devido a localização"""
        non_plant_events = []
        plant_events = self.get_plants()
        for i in self.get_supervisor():
            if i not in plant_events:
                non_plant_events.append(i)
        return non_plant_events

    def set_controlable(self):
        non_plant_events = self.non_plant_event()
        for i in self.get_supervisor():
            controlable = i.get_controlable()
            for j in controlable:
                if j[1] in non_plant_events:
                    i.remove_controlable(j)

    def set_pin(self):
        """Set se os pinos sao entrada ou saida, de acordo com a localização"""
        code = "\n\n"
        inp = "INPUT"
        out = 'OUTPUT'
        for j in self.get_supervisor():
            events = j.get_events()
            for i in sorted(events):
                if int(i) % 2 == 0:
                    code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", inp], ident=1)
                elif int(i) % 2 != 0 and i in self.non_plant_event():
                    code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", out], ident=1)
                else:
                    code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", out], ident=1)
        return code
