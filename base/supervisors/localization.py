from .modular_local import ModularLocal


class SupervisorLocalizado(ModularLocal):
    def __init__(self, language, user=None):
        super().__init__(language, user)
        self.non_plant_events = []

    def _set_events(self):
        if not self.non_plant_events:
            self.set_non_plant_event()
        for i in self.supervisors:
            if not i.avalanche_checked:
                i.check_avalanche()
            controlable_events = i.get_controlable()
            non_controlable_events = i.get_non_controlable()
            for j in controlable_events:
                if j[1] not in self.non_plant_events:
                    self.controlable_events.add(j[1])
                else:
                    self.non_controlable_events.add(j[1])
            for j in non_controlable_events:
                self.non_controlable_events.add(j[1])

    def set_transitions(self):
        super().set_transitions()
        controlable = self.controlable.copy()
        for i in self.controlable:
            if i[1] in self.get_non_controlable_events():
                controlable.remove(i)
                self.non_controlable.append(i)
        self.controlable = controlable
        print(self.controlable)

    def set_non_plant_event(self):
        """Encontra os eventos não controláveis devido a localização"""
        plants = self.get_plants()
        plant_events = plants[0].get_events()
        for i in self.get_supervisor():
            events = i.get_events()
            for j in events:
                if j not in plant_events:
                    self.non_plant_events.append(j)

    def get_non_plant_events(self):
        if not self.non_plant_events:
            self.set_non_plant_event()
        return sorted(self.non_plant_events)

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
                elif int(i) % 2 != 0 and i in self.get_non_plant_events():
                    code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", inp], ident=1)
                else:
                    code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", out], ident=1)
        return code
