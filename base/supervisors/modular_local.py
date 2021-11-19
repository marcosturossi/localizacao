from datetime import datetime
from base.language.c import C, Arduino


class Supervisor:
    def __init__(self, language):
        self.plants = {}
        self.supervisors = {}
        self.lang = language
        self.plant_events = None
        self.supervisor_events = None
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
        self.plants[data['plant']['name']] = data['plant']
        self.supervisors[data['supervisor']['name']] = data['supervisor']

    def check_avalanche(self, data):
        avalanche_list = []
        avalanche = False
        for key, values in data.items():
            for i in range(len(values)):
                for j in range(1, len(values)):
                    if values[i][1] == values[j][1] and i != j:
                        if values[i][2] == values[j][0]:
                            avalanche_list.append(values[i])
                            avalanche_list.append(values[j])
                            avalanche = True
            for i in avalanche_list:
                if avalanche_list.count(i) > 1:
                    avalanche_list.remove(i)
            if avalanche is True:
                self.avalanche[key] = avalanche_list
                self.split_avalanche(key)
        return avalanche

    def split_avalanche(self, name):
        crescent = []
        decrescent = []
        non_avalanche = []
        new_transitions = []
        for i in self.avalanche[name]:
            if int(i[0]) < int(i[2]):
                crescent.append(i)
            else:
                decrescent.append(i)
        crescent = sorted(crescent, reverse=True)
        decrescent = sorted(decrescent)
        for i in self.supervisors.values():
            if i['name'] == name:
                for j in i['transitions']:
                    if j not in crescent and j not in decrescent and j[0] != j[2]:
                        non_avalanche.append(j)
        for i in crescent:
            new_transitions.append(i)
        for i in decrescent:
            new_transitions.append(i)
        for i in non_avalanche:
            new_transitions.append(i)
        self.new_transitions[name] = new_transitions

    # def check_choice_problem(self):
    #     # TODO não implantando ainda
    #     """Verifica se existe o problema de escolha no supervisor"""
    #     for i in range(len(self.supervisor_transitions)):
    #         for j in range(1, len(self.supervisor_transitions)):
    #             if self.supervisor_transitions[i][1] == self.supervisor_transitions[j][1] and i != j and int(
    #                     self.supervisor_transitions[i][1]) % 2 != 0 and \
    #                     self.supervisor_transitions[i][0] == self.supervisor_transitions[j][0]:
    #                 self.choice_problem_list.append(self.supervisor_transitions[i])
    #                 self.choice_problem_list.append(self.supervisor_transitions[j])
    #                 self.choice_problem = True
    #     if self.choice_problem is None:
    #         self.choice_problem = False
    #     return self.choice_problem

    def set_events(self):
        """Separar os por set"""
        self.plant_events = []
        self.supervisor_events = []
        self.all_events = []
        for i in self.plants.values():
            for j in i['transitions']:
                self.plant_events.append(j[1])
                self.all_events.append(j[1])
        for i in self.supervisors.values():
            for j in i['transitions']:
                self.supervisor_events.append(j[1])
                self.all_events.append(j[1])
        self.plant_events = set(self.plant_events)
        self.supervisor_events = set(self.supervisor_events)
        self.all_events = set(self.all_events)

    def set_transitions(self):
        """Separar as transições em controlável e não controláveis"""
        for i in self.supervisors.values():
            non_controlable = []
            controlable = []
            for j in i['transitions']:
                if int(j[1]) % 2 == 0:
                    non_controlable.append(j.copy())
                else:
                    controlable.append(j.copy())
            self.non_controlable[i['name']] = non_controlable
            self.controlable[i['name']] = controlable

    def get_events(self):
        """Recupera os eventos"""
        if self.plant_events is None and self.supervisor_events is None:
            self.set_events()
        return self.plant_events, self.supervisor_events

    def set_state(self):
        for i in self.plants.values():
            state = set()
            for j in i['transitions']:
                state.add(j[0])
                state.add(j[2])
            self.plant_states[i['name']] = state
        for i in self.supervisors.values():
            state = set()
            for j in i['transitions']:
                state.add(j[0])
                state.add(j[2])
            self.supervisor_states[i['name']] = state

    def get_states(self):
        if self.plant_states is {} and self.supervisor_states is {}:
            self.set_state()
        return self.plant_states, self.supervisor_states

    def set_prevent_events(self):
        all_possibility = {}
        prevent_event = {}

        if self.controlable == {}:
            self.set_transitions()

        # Cria todas as possibilidades
        for k, v in self.controlable.items():
            for key, value in self.supervisors.items():
                all_list = []
                if key == k:
                    for h in v:
                        for g in value['transitions']:
                            if [g[0], h[1]] not in all_list:
                                all_list.append([g[0], h[1]])
                    all_possibility[k] = all_list

        # Retira o ultimo elemento de todos os eventos
        controlable = {}
        for i in self.controlable:
            controlable_list = []
            for j in self.controlable[i]:
                controlable_list.append([j[0], j[1]])
            controlable[i] = controlable_list

        for i in all_possibility:
            for j in controlable:
                prevent_event_list = []
                if i == j:
                    for h in all_possibility[i]:
                        if h not in controlable[j]:
                            prevent_event_list.append(h)
                    prevent_event[i] = prevent_event_list
        self.prevent_events = prevent_event

    def get_prevent_events(self):
        if self.prevent_events is None:
            self.set_prevent_events()
        return self.prevent_events

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

    def format_var(self):
        """Formata as variáveis e retorna todos"""
        if self.plant_events is None:
            self.set_events()
        events = self.all_events
        formated_var = []
        for i in sorted(events):
            formated_var.append(f'EV{i}')
        return formated_var

    def declared_var(self):
        var = self.format_var()
        code = ""
        for i in var:
            code += self.lang.o_declare_var('bool', i, 0, 1)
        return code

    def declare_last_state(self):
        """Declara as para armazenar os ultimo estado dos eventos não controláveis"""
        code = ""
        non_controlable = set()
        if self.non_controlable == {}:
            self.set_transitions()
        for i in self.non_controlable:
            for j in self.non_controlable[i]:
                non_controlable.add(j[1])
        for i in non_controlable:
            code += self.lang.o_declare_var('bool', f"LS_EV{i}", 0, 1)
        for i in non_controlable:
            code += self.lang.o_declare_var('bool', f"IN{i}", 0, 1)
        return code

    def declare_state(self):
        code = ""
        if self.plant_states is {} and self.supervisor_states is {}:
            self.set_state()
        for i in self.plant_states:
            code += self.lang.o_create_array(i, self.plant_states[i], ident=1)
        for i in self.supervisor_states:
            code += self.lang.o_create_array(i, self.supervisor_states[i], ident=1)
        return code

    def declare_prevent_state(self):
        prevent_events = set()
        if self.prevent_events is None:
            self.set_prevent_events()
        for i in self.prevent_events.values():
            for j in i:
                prevent_events.add(j[1])
        code = "    // Eventos desabilitados pelo supervisor \n"
        if self.prevent_events is None:
            self.get_prevent_events()
        for i in prevent_events:
            code += self.lang.o_declare_var('bool', f'D_EV{i}', 0, 1)
        code += "\n"
        return code

    def declare_pin(self):
        code = "// Definição dos saida GPIO\n"
        j = 1
        for i in self.format_var():
            code += self.lang.o_declare_var('int', f"{i}PIN", j, ident=1)
            j += 1
        return code

    def read_inputs(self):
        """Inicia o código com a leitura das variáveis"""
        code = "        //Inicia a leitura das entradas \n"
        var = self.format_var()
        for i in range(len(sorted(self.all_events))):
            if int(var[i][-1]) % 2 == 0:
                code += self.lang.o_call_function('digitalRead', [f"{var[i]}PIN"], f"IN{var[i][-1]}", 2)
        return code

    def format_prevent_events(self):
        op1 = 'if'
        """Desabilitação dos Eventos Controláveis pelo supervisor"""
        code = "\n        // Desabilitação dos Eventos Controláveis pelo Supervisor\n"
        for key, value in self.prevent_events.items():
            for i in value:
                condiction = f"{self.lang.o_array_name(key, i[0])} == 1"
                action = {f"D_EV{i[1]}": 1}
                code += self.lang.o_if(op1, condiction, action, 2)
        return code

    def update_plant_state(self):
        op1 = 'if'
        code = "\n        // Atualização dos Estados da planta pelos eventos não controláveis\n"
        for i in self.plants.values():
            for j in i['transitions']:
                if int(j[1]) % 2 == 0:
                    condiction = f"{self.lang.o_array_name(i['name'], j[0])} == 1 {self.lang.oand} " \
                                 f"D_EV{j[1]} == 0"
                    action = {f"{self.lang.o_array_name(i['name'], j[0])}": 0,
                              f"{self.lang.o_array_name(i['name'], j[2])}": 1}
                    code += self.lang.o_if(op1, condiction, action, 2)
            return code

    def update_state(self, transitions):
        op1 = 'if'
        """Atualização dos modelos da planta e do supervisor de acordo com os eventos não controláveis"""
        code = f"\n        //Atualiza os estados\n"
        avanlanche = self.check_avalanche(transitions)
        if avanlanche is True:
            transitions = self.new_transitions
        for key, values in transitions.items():
            for i in values:
                condiction = f"{self.lang.o_array_name(key, i[0])} == 1 {self.lang.oand} EV{i[1]} == HIGH"
                action = {f"{self.lang.o_array_name(key, i[0])}": 0,
                          f"{self.lang.o_array_name(key, i[2])}": 1}
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
        for i in self.plants.values():
            for j in i['transitions']:
                if int(j[1]) % 2 != 0:
                    condiction = f"{self.lang.o_array_name(i['name'], j[0])} == 1 {self.lang.oand} " \
                                 f"D_EV{j[1]} == 0"
                    action = {f"{self.lang.o_array_name(i['name'], j[0])}": 0,
                              f"{self.lang.o_array_name(i['name'], j[2])}": 1,
                              F"EV{j[1]}": 1}
                    code += self.lang.o_if(op1, condiction, action, 2)
            return code

    def set_pin(self):
        """São Criado os Pinos de entrada e Saida"""
        code = "    // Declara os GPIO Pin\n"
        inp = 'INPUT'
        out = 'OUTPUT'
        for i in sorted(self.all_events):
            if int(i) % 2 == 0:
                code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", inp], ident=1)
            else:
                code += self.lang.o_call_function('pinMode', [f"EV{i}PIN", out], ident=1)
        return code


    def write_outputs(self):
        code = "        // Escreve os eventos na saida\n"
        for i in self.plant_events:
            if int(i) % 2 != 0:
                condition = f"EV{i} == 1"
                action_if = f"EV{i}PIN = HIGH"
                action_else = f"EV{i}PIN = LOW"
                code += self.lang.o_if_else(condition, action_if, action_else, 2)
        return code


    def create_loop(self, action):
        code = self.lang.o_loop(action, 1, 1)
        return code


    def createcode_c(self):
        """ Chama a os métodos para a contrução do código"""
        # Declara o inicio do código
        self.set_state()
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
        code_in_loop += self.update_state(self.non_controlable)
        code_in_loop += self.format_prevent_events()
        code_in_loop += self.generate_controlable_events()
        code_in_loop += self.update_state(self.controlable)
        code_in_loop += self.write_outputs()
        if self.lang.__class__ == C:
            code_in_main += self.create_loop(code_in_loop)
            code += self.start_function(code_in_main)
        elif self.lang.__class__ == Arduino:
            code += self.start_function(code_in_main)
            code += self.create_loop(code_in_loop)
        return str(code)
