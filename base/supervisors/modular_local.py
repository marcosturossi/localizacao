from datetime import datetime
from base.language.c import C, Arduino


class ModularLocal:
    def __init__(self, language):
        self.automatos = []
        self.lang = language
        self.plants = []
        self.supervisors = []
        self.all_events = None
        self.plant_states = {}
        self.supervisor_states = {}
        self.all_states = {}
        self.prevent_events = None
        self.avalanche = {}
        self.new_transitions = {}
        self.controlable = {}
        self.non_controlable = {}

    def set_data(self, data):
        self.automatos.append(data)

    def split_automatos(self):
        for i in self.automatos:
            if i.__class__.__name__ == "Plant":
                self.plants.append(i)
            else:
                self.supervisors.append(i)

    def create_header(self):
        data = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        universidade = 'Universidade do Estado de Santa Catarina'
        return self.lang.o_create_header(data, universidade, 'Anonymous')

    def create_import(self):
        code = self.lang.o_import('wiringPi.h')
        return code

    def start_function(self, value):
        code = "\n"
        code += self.lang.o_declare_function('int', 'main', value)
        return code

    def declared_var(self):
        code = ""
        for i in self.supervisors:
            named_events = i.get_named_events()
            for j in named_events.values():
                code += self.lang.o_declare_var('bool', j, 0, 1)
        return code

    def declare_last_state(self):
        """Declara as para armazenar os ultimo estado dos eventos não controláveis"""
        code = ""
        non_controlable = set()
        for i in self.supervisors:
            events_non_controlable = i.get_non_controlable()
            for i in events_non_controlable:
                non_controlable.add(i[1])
            for i in non_controlable:
                code += self.lang.o_declare_var('bool', f"LS_EV{i}", 0, 1)
            for i in non_controlable:
                code += self.lang.o_declare_var('bool', f"IN{i}", 0, 1)
        return code

    def declare_state(self):
        code = ""
        for i in self.automatos:
            code += self.lang.o_create_array(i.get_name(), i.get_states(), ident=1)
        return code

    def declare_prevent_state(self):
        code = "    // Eventos desabilitados pelo supervisor \n"
        for i in self.supervisors:
            prevent_events = i.get_prevent_events()
            for i in prevent_events:
                code += self.lang.o_declare_var('bool', f'D_EV{i}', 0, 1)
            code += "\n"
        return code

    def declare_pin(self):
        code = "// Definição dos saida GPIO\n"
        j = 1
        for i in self.supervisors:
            named_events = i.get_named_events()
            for key in named_events:
                code += self.lang.o_declare_var('int', f"{key}PIN", j, ident=1)
                j += 1
        return code

    def read_inputs(self):
        """Inicia o código com a leitura das variáveis"""
        code = "        //Inicia a leitura das entradas \n"
        for i in self.supervisors:
            var = i.get_named_events()
            for j in var:
                if int(var[j][-1]) % 2 == 0:
                    code += self.lang.o_call_function('digitalRead', [f"{var[j]}PIN"], f"IN{var[j][-1]}", 2)
        return code

    def format_prevent_events(self):
        op1 = 'if'
        """Desabilitação dos Eventos Controláveis pelo supervisor"""
        code = "\n        // Desabilitação dos Eventos Controláveis pelo Supervisor\n"
        for i in self.supervisors:
            prevent_events = i.get_prevent_events()
            for j in prevent_events:
                condiction = f"{self.lang.o_array_name(i.get_name(), j[0])} == 1"
                action = {f"D_EV{j[1]}": 1}
                code += self.lang.o_if(op1, condiction, action, 2)
        return code

    def update_plant_state(self):
        op1 = 'if'
        code = "\n        // Atualização dos Estados da planta pelos eventos não controláveis\n"
        for i in self.plants:
            for j in i.get_non_controlable():
                if int(j[1]) % 2 == 0:
                    condiction = f"{self.lang.o_array_name(i.get_name(), j[0])} == 1 {self.lang.oand} " \
                                 f"D_EV{j[1]} == 0"
                    action = {f"{self.lang.o_array_name(i.get_name(), j[0])}": 0,
                              f"{self.lang.o_array_name(i.get_name(), j[2])}": 1}
                    code += self.lang.o_if(op1, condiction, action, 2)
        return code

    def update_state(self, controlable=False):
        op1 = 'if'
        """Atualização dos modelos da planta e do supervisor de acordo com os eventos não controláveis"""
        code = f"\n        //Atualiza os estados\n"
        for i in self.supervisors:
            i.check_avalanche()
            if controlable:
                transitions = i.get_controlable()
            else:
                transitions = i.get_non_controlable()
            for j in transitions:
                condiction = f"{self.lang.o_array_name(i.get_name(), j[0])} == 1 {self.lang.oand} EV{j[1]} == HIGH"
                action = {f"{self.lang.o_array_name(i.get_name(), j[0])}": 0,
                          f"{self.lang.o_array_name(i.get_name(), j[2])}": 1}
                code += self.lang.o_if(op1, condiction, action, 2)
        return code

    def generate_noncontrolable_events(self):
        code = ""
        non_controlable = set()
        for i in self.non_controlable:
            for j in self.non_controlable[i]:
                non_controlable.add(j[1])
        for i in non_controlable:
            condition = f"IN{i} != LS_EV{i} && IN{i} == HIGH"
            action_if = f'EV{i} == 1;\n            LS_EV{i} == EV{i}'
            action_else = f'EV{i} == 0'
            code += self.lang.o_if_else(condition, action_if, action_else, 2)
        return code

    def generate_controlable_events(self):
        op1 = 'if'
        code = "\n        // Geração dos eventos Controláveis e atualização dos estados da planta\n"
        for i in self.plants:
            controlable = i.get_controlable()
            for j in controlable:
                condiction = f"{self.lang.o_array_name(i.get_name(), j[0])} == 1 {self.lang.oand} " \
                             f"D_EV{j[1]} == 0"
                action = {f"{self.lang.o_array_name(i.get_name(), j[0])}": 0,
                          f"{self.lang.o_array_name(i.get_name(), j[2])}": 1,
                          F"EV{j[1]}": 1}
                code += self.lang.o_if(op1, condiction, action, 2)
        return code

    def set_pin(self):
        """São Criado os Pinos de entrada e Saida"""
        code = "    // Declara os GPIO Pin\n"
        inp = 'INPUT'
        out = 'OUTPUT'
        for i in self.plants:
            events = sorted(i.get_events())
            for i in events:
                if int(i) % 2 == 0:
                    code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", inp], ident=1)
                else:
                    code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", out], ident=1)
        return code

    def write_outputs(self):
        code = "        // Escreve os eventos na saida\n"
        for i in self.plants:
            named_events = i.get_named_events()
            for key, value in named_events.items():
                if int(key) % 2 != 0:
                    condition = f"{key} == 1"
                    action_if = f"{key}PIN = HIGH"
                    action_else = f"{key}PIN = LOW"
                    code += self.lang.o_if_else(condition, action_if, action_else, 2)
        return code

    def create_loop(self, action):
        code = self.lang.o_loop(action, 1, 1)
        return code

    def createcode(self):
        """ Chama a os métodos para a contrução do código"""
        # Declara o inicio do código
        self.split_automatos()
        code = self.create_header()
        code += self.create_import()
        code_in_main = self.declare_pin()
        code_in_main += self.declare_state()
        code_in_main += self.set_pin()
        code_in_main += self.declared_var()
        code_in_main += self.declare_last_state()

        # Inicia a lógica de Controle
        code_in_loop = self.declare_prevent_state()
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
