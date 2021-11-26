from datetime import datetime
from base.language.c import C, Arduino


class ModularLocal:
    def __init__(self, language, user=None):
        self.automatos = []
        self.lang = language
        if user:
            self.user = user
        else:
            self.user = "Anonymous"
        self.plants = []
        self.supervisors = []
        self.controlable_events = set()
        self.non_controlable_events = set()
        self.controlable = []
        self.non_controlable = []

    def set_data(self, data):
        self.automatos.append(data)

    def get_supervisor(self):
        if not self.supervisors:
            self._split_automatos()
        return self.supervisors

    def get_controlable_events(self):
        if not self.controlable_events:
            self._set_events()
        return self.controlable_events

    def get_non_controlable_events(self):
        if not self.non_controlable_events:
            self._set_events()
        return self.non_controlable_events

    def set_transitions(self):
        for i in self.supervisors:
            transitions = i.get_transitions()
            for i in transitions:
                if int(i[1]) % 2 == 0:
                    self.non_controlable.append(i)
                else:
                    self.controlable.append(i)

    def get_controlable(self):
        if not self.controlable:
            self.set_transitions()
        return self.controlable

    def get_non_controlable(self):
        if not self.non_controlable:
            self.set_transitions()
        return self.non_controlable

    def _set_events(self):
        """Separa os eventos controláveis e não controláveis"""
        for i in self.supervisors:
            if not i.avalanche_checked:
                i.check_avalanche()
            controlable_events = i.get_controlable()
            non_controlable_events = i.get_non_controlable()
            for j in controlable_events:
                self.controlable_events.add(j[1])
            for j in non_controlable_events:
                self.non_controlable_events.add(j[1])

    def get_plants(self):
        if not self.plants:
            self._split_automatos()
        return self.plants

    def _split_automatos(self):
        for i in self.automatos:
            if i.__class__.__name__ == "Plant":
                self.plants.append(i)
            else:
                self.supervisors.append(i)

    def create_header(self):
        data = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        universidade = 'Universidade do Estado de Santa Catarina'
        obs = "O X foi utilizado abaixo afim de representar um valor numérico das variáveis\n" \
              "EVXPIN = Declaração dos pinos de utilizados de hardware\n" \
              "EVX = Declaração dos Eventos\n" \
              "LS_EVX = Armazena o ultimo estado (borda de subida)\n" \
              "INX = Variável que guarda os valores lidos no pinos de entrada\n" \
              "D_EVX = Desabilitação dos eventos controláveis pela planta"
        return self.lang.o_create_header(data, universidade, self.user, obs)

    def create_import(self):
        if self.lang.__class__.__name__ == 'Arduino':
            code = ""
        else:
            code = self.lang.o_import('wiringPi.h')
        return code

    def start_function(self, value):
        code = "\n"
        if self.lang.__class__.__name__ == 'Arduino':
            code += self.lang.o_declare_function('void', 'setup', value)
        else:
            code += self.lang.o_declare_function('int', 'main', value)

        return code

    def declared_var(self):
        code = self.lang.o_coment("Declaração de Eventos", 0)
        duplicated = []
        for i in self.get_supervisor():
            named_events = i.get_named_events()
            for j in named_events.values():
                if j not in duplicated:
                    duplicated.append(j)
                    code += self.lang.o_declare_var('bool', j, 0, 1)
        return code

    def declare_last_state(self):
        """Declara as para armazenar os ultimo estado dos eventos não controláveis"""
        code = self.lang.o_coment("Variáveis de Entrada e Memoria para Borda de Subida", 0)
        duplicated = []
        for i in self.get_non_controlable_events():
            if i not in duplicated:
                duplicated.append(i)
                code += self.lang.o_declare_var('int', f"LS_EV{i}", 0, 0)
                code += self.lang.o_declare_var('int', f"IN{i}", 0, 0)
        return code

    def declare_state(self):
        code = self.lang.o_coment("Declaração de Estados", 0)
        for i in self.automatos:
            code += self.lang.o_create_array('int', i.get_name(), i.get_states(), ident=0)
        return code

    def declare_prevent_state(self):
        code = self.lang.o_coment("Eventos desabilitados pelo supervisor", 1)
        just_events = set()
        for i in self.get_supervisor():
            prevent_events = i.get_prevent_events()
            for j in prevent_events:
                if j[1] not in self.non_controlable_events:
                    just_events.add(j[1])
        for i in just_events:
            code += self.lang.o_declare_var('int', f'D_EV{i}', 0, 1)

        return code + "\n"

    def declare_pin(self):
        code = self.lang.o_coment("Definição dos saida GPIO", 0)
        j = 1
        duplicated = []
        for i in self.get_supervisor():
            named_events = i.get_named_events()
            for value in named_events.values():
                if value not in duplicated:
                    duplicated.append(value)
                    code += self.lang.o_declare_var('int', f"{value}Pin", j, ident=0)
                j += 1
        return code

    def read_inputs(self):
        """Inicia o código com a leitura das variáveis"""
        code = self.lang.o_coment("Inicia a leitura das entradas", 1)
        for i in self.get_non_controlable_events():
            code += self.lang.o_call_function('digitalRead', [f"EV{i}Pin"], f"IN{i}", 1)
        return code + "\n"

    def format_prevent_events(self):
        op1 = 'if'
        """Desabilitação dos Eventos Controláveis pelo supervisor"""
        code = self.lang.o_coment("Desabilitação dos Eventos Controláveis pelo Supervisor", 1)
        for i in self.get_supervisor():
            prevent_events = i.get_prevent_events()
            for j in prevent_events:
                if j[1] not in self.get_non_controlable_events():
                    condiction = f"{self.lang.o_array_name(i.get_name(), j[0])} == 1"
                    action = {f"D_EV{j[1]}": 1}
                    code += self.lang.o_if(op1, condiction, action, 1)
        return code

    def update_plant_state(self):
        op1 = 'if'
        code = self.lang.o_coment("Atualização dos Estados da planta pelos eventos não controláveis", 1)
        for i in self.plants:
            for j in i.get_non_controlable():
                condiction = f"{self.lang.o_array_name(i.get_name(), j[0])} == 1 {self.lang.oand} " \
                             f"EV{j[1]} == 1"
                action = {f"{self.lang.o_array_name(i.get_name(), j[0])}": 0,
                          f"{self.lang.o_array_name(i.get_name(), j[2])}": 1}
                code += self.lang.o_if(op1, condiction, action, 1)
        return code

    def update_state(self, controlable=False):
        op1 = 'if'
        """Atualização dos modelos do supervisor de acordo com os controláveis e não controláveis"""
        if controlable:
            var = 'controlável'
        else:
            var = 'não controlável'
        code = self.lang.o_coment(f"Atualização dos Estados da Supervisor pelos Eventos {var}", 1)
        for i in self.get_supervisor():
            if not i.avalanche_checked:
                i.check_avalanche()
            if controlable:
                transitions = self.get_controlable()
            else:
                transitions = self.get_non_controlable()
            for j in transitions:
                if j[0] != j[2]:
                    condiction = f"{self.lang.o_array_name(i.get_name(), j[0])} == 1 {self.lang.oand} EV{j[1]} == 1"
                    action = {f"{self.lang.o_array_name(i.get_name(), j[0])}": 0,
                              f"{self.lang.o_array_name(i.get_name(), j[2])}": 1}
                    code += self.lang.o_if(op1, condiction, action, 1)
        return code

    def generate_noncontrolable_events(self):
        code = self.lang.o_coment("Identificação da Borda de Subida", 1)
        for i in self.get_supervisor():
            if not i.avalanche_checked:
                i.check_avalanche()
        for i in self.non_controlable_events:
            condition = f"IN{i} != LS_EV{i} {self.lang.oand} IN{i} == HIGH"
            action_if = f'EV{i} = 1;\n        LS_EV{i} = EV{i}'
            action_else = f'LS_EV{i} = IN{i}'
            code += self.lang.o_if_else(condition, action_if, action_else, 1)
        return code

    def generate_controlable_events(self):
        op1 = 'if'
        code = self.lang.o_coment("Geração dos eventos Controláveis e atualização dos estados da planta", 1)
        for i in self.plants:
            controlable = i.get_controlable()
            for j in controlable:
                condiction = f"{self.lang.o_array_name(i.get_name(), j[0])} == 1 {self.lang.oand} " \
                             f"D_EV{j[1]} == 0"
                action = {f"{self.lang.o_array_name(i.get_name(), j[0])}": 0,
                          f"{self.lang.o_array_name(i.get_name(), j[2])}": 1,
                          F"EV{j[1]}": 1}
                code += self.lang.o_if(op1, condiction, action, 1)
        return code

    def set_pin(self):
        """São Criado os Pinos de entrada e Saida"""
        code = self.lang.o_coment("Declara os GPIO Pin", 1)
        inp = 'INPUT'
        out = 'OUTPUT'
        for i in self.plants:
            events = sorted(i.get_events())
            for j in events:
                if int(j) % 2 == 0:
                    code += self.lang.o_call_function('pinMode', [f"EV{j}Pin", inp], ident=1)
                else:
                    code += self.lang.o_call_function('pinMode', [f"EV{j}Pin", out], ident=1)
        return code

    def write_outputs(self):
        code = self.lang.o_coment("Escreve os eventos na saida", 1)
        for i in self.plants:
            correlanted, non_correlarted = i.get_correlated_events()
            for j in correlanted:
                pin = ""
                for key, value in j.items():
                    op = "if"
                    if int(key) % 2 != 0:
                        condition = f"{value} == 1"
                        param = [value + 'Pin', 'HIGH']
                        code += self.lang.o_write_output(op, condition, param, 1)
                        pin = value
                    else:
                        if self.lang.__class__.__name__ == 'Arduino':
                            op = 'else if'
                        else:
                            op = 'elif'
                        condition = f"{value} == 1"
                        param = [pin + 'Pin', 'LOW']
                        code += self.lang.o_write_output(op, condition, param, 1)
            if non_correlarted:
                for j in non_correlarted:
                    for key, value in j.items():
                        condition = f"{value} == 0"
                        param = [value + 'Pin', 'HIGH']
                        code += self.lang.o_write_output('if', condition, param, 1)
        return code

    def create_loop(self, action):
        code = self.lang.o_loop(action, 1, 1)
        return code

    def createcode(self):
        """ Chama a os métodos para a contrução do código"""
        # Declara o inicio do código
        code = self.create_header()
        code += self.create_import()
        code += self.declare_pin()
        code += self.declare_state()
        code += self.declare_last_state()
        code_in_main = self.set_pin()

        # Inicia a lógica de Controle
        code_in_loop = self.declared_var()
        code_in_loop += self.declare_prevent_state()
        code_in_loop += self.read_inputs()
        code_in_loop += self.generate_noncontrolable_events()
        code_in_loop += self.update_plant_state()
        code_in_loop += self.update_state(controlable=False)
        code_in_loop += self.format_prevent_events()
        code_in_loop += self.generate_controlable_events()
        code_in_loop += self.update_state(controlable=True)
        code_in_loop += self.write_outputs()
        if self.lang.__class__ == C:
            code_in_main += self.create_loop(code_in_loop)
            code += self.start_function(code_in_main)
        elif self.lang.__class__ == Arduino:
            code += self.start_function(code_in_main)
            code += self.create_loop(code_in_loop)
        return str(code)
