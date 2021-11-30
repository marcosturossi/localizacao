from .modular_local import ModularLocal


class SupervisorLocalizado(ModularLocal):
    def __init__(self, language, user=None):
        super().__init__(language, user)
        self.non_plant_events = []

    def declared_var(self):
        code = self.lang.o_coment("Declaração de Eventos", 0)
        duplicated = []
        for i in self.get_supervisor():
            named_events = i.get_named_events()
            for j in named_events.values():
                if j not in duplicated:
                    duplicated.append(j)
                    code += self.lang.o_declare_var('bool', j, 0, 1)
        for i in self.get_plants():
            named_events = i.get_named_events()
            for j in named_events.values():
                if j not in duplicated:
                    duplicated.append(j)
                    code += self.lang.o_declare_var('bool', j, 0, 1)
        return code

    def declare_pin(self):
        code = self.lang.o_coment("Definição dos saida GPIO", 0)
        j = 1
        duplicated = []
        for i in self.automatos:
            named_events = i.get_named_events()
            for value in named_events.values():
                if value not in duplicated:
                    duplicated.append(value)
                    code += self.lang.o_declare_var('int', f"{value}Pin", j, ident=0)
                j += 1
        return code

    def _set_events(self):
        if not self.non_plant_events:
            self.set_non_plant_event()
        for i in self.automatos:
            if i.__class__.__name__ == "Supervisor":
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

    def update_state(self, controlable=False):
        for i in self.get_supervisor():
            trans_controlable = i.get_controlable()
            for j in trans_controlable:
                if j[1] in self.non_plant_events:
                    i.remove_controlable(j)
        return super().update_state(controlable)

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
        duplicated = []
        for j in self.automatos:
            events = j.get_events()
            for i in sorted(events):
                if i not in duplicated:
                    duplicated.append(i)
                    if int(i) % 2 == 0:
                        code += self.lang.o_call_function('pinMode', [f"EV{i}Pin", inp], ident=1)
                    elif int(i) % 2 != 0 and i in self.get_non_plant_events():
                        code += self.lang.o_call_function('pinMode', [f"EV{i}Pin", inp], ident=1)
                    else:
                        code += self.lang.o_call_function('pinMode', [f"EV{i}Pin", out], ident=1)
        return code
