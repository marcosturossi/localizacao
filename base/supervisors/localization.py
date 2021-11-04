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

    def setup_pin(self):
        """Set se os pinos sao entrada ou saida, de acordo com a localização"""
        code = "\n\n"
        if self.language == "C":
            inp = "INPUT"
            out = 'OUTPUT'
            for i in sorted(self.all_events):
                if int(i) % 2 == 0:
                    code += f'    pinMode(EV{i}Pin, {inp}); \n'
                elif int(i) % 2 != 0 and i in self.non_plant_event():
                    code += f'    pinMode(EV{i}Pin, {out}); \n'
                else:
                    code += f'    pinMode(EV{i}Pin, {out}); \n'
        return code

    def createcode_c(self):
        """ Chama a os métodos para a contrução do código"""
        # Declara o inicio do código
        print(self.plants)
        print(self.supervisors)
        code = self.create_header()
        code += self.create_import()
        code += self.declare_pin()
        code += self.declare_state()
        code += self.start_function()
        code += self.setup_pin()

        # Inicia a lógica de Controle
        code += self.create_loop()
        code += self.declared_var()
        code += self.declare_prevent_state()
        code += self.read_inputs()
        code += self.update_state_nc(self.plant_transitions, 'p_state')
        code += self.corret_avalanche()
        code += self.format_prevent_events()
        code += self.generate_controlable_events()
        code += self.update_supervisor_states()
        code += self.write_outputs()
        code += self.close_program()
        return str(code)
