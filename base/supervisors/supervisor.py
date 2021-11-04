from datetime import datetime


class Supervisor:
    def __init__(self, language):
        self.plants = []
        self.supervisors = []
        self.language = language
        self.plant_events = None
        self.supervisor_events = None
        self.all_events = None
        self.plant_states = None
        self.supervisor_states = None
        self.all_states = None
        self.prevent_events = None
        self.avalanche = None
        self.avalanche_list = []
        self.non_avalanche_list = []
        self.choice_problem = None
        self.choice_problem_list = []
        self.crescent_avalanche = []
        self.decrescent_avalanche = []

    def set_data(self, data):
        self.plants.append(data['plant'])
        self.supervisors.append(data['supervisor'])

    def check_avalanche(self):
        for i in range(len(self.supervisor_transitions)):
            for j in range(1, len(self.supervisor_transitions)):
                if self.supervisor_transitions[i][1] == self.supervisor_transitions[j][1] and i != j:
                    if self.supervisor_transitions[i][2] == self.supervisor_transitions[j][0]:
                        self.avalanche_list.append(self.supervisor_transitions[i])
                        self.avalanche_list.append(self.supervisor_transitions[j])
                        self.avalanche = True
        for i in self.avalanche_list:
            if self.avalanche_list.count(i) > 1:
                self.avalanche_list.remove(i)
        if self.avalanche is None:
            self.avalanche = False
        else:
            self.split_avalanche()
        return self.avalanche

    def check_choice_problem(self):
        # TODO não implantando ainda
        """Verifica se existe o problema de escolha no supervisor"""
        for i in range(len(self.supervisor_transitions)):
            for j in range(1, len(self.supervisor_transitions)):
                if self.supervisor_transitions[i][1] == self.supervisor_transitions[j][1] and i != j and int(
                        self.supervisor_transitions[i][1]) % 2 != 0 and \
                        self.supervisor_transitions[i][0] == self.supervisor_transitions[j][0]:
                    self.choice_problem_list.append(self.supervisor_transitions[i])
                    self.choice_problem_list.append(self.supervisor_transitions[j])
                    self.choice_problem = True
        if self.choice_problem is None:
            self.choice_problem = False
        return self.choice_problem

    def set_events(self):
        """Adiciona os eventos aos atributos"""
        self.plant_events = []
        self.supervisor_events = []
        self.all_events = []
        for i in self.plants:
            for j in i['transitions']:
                self.plant_events.append(j[1])
                self.all_events.append(j[1])
        for i in self.supervisors:
            for j in i['transitions']:
                self.plant_events.append(j[1])
                self.all_events.append(j[1])
        set(self.plant_events)
        set(self.supervisor_events)
        set(self.all_events)

    def get_events(self):
        """Recupera os eventos"""
        if self.plant_events is None and self.supervisor_events is None:
            self.set_events()
        return self.plant_events, self.supervisor_events

    def set_state(self):
        self.plant_states = {}
        self.supervisor_states = {}
        self.all_states = {}
        for i in self.plants:
            state = set()
            for j in i['transitions']:
                state.add(j[0])
                state.add(j[2])
                state.add(j[0])
                state.add(j[1])
            self.plant_states[i['name']] = state
        for i in self.supervisors:
            state = set()
            for j in i['transitions']:
                state.add(j[0])
                state.add(j[2])
                state.add(j[0])
                state.add(j[1])
            self.plant_states[i['name']] = state

    def get_states(self):
        if self.plant_states is None and self.supervisor_states is None:
            self.set_state()
        return self.plant_states, self.supervisor_states

    def set_prevent_events(self):
        all_possibility = {}
        controlable_transitions = {}
        prevent_event = {}

        for i in self.supervisors:
            controlable = []
            for j in i['transitions']:
                if int(j[1]) % 2 != 0:
                    controlable.append([j[0], j[1]])
            controlable_transitions[i['name']] = controlable_transitions

        # Cria todas as possibilidades
        for i in controlable_transitions:
            for j in self.supervisor_states:
                all_list = []
                if i['name'] == j['name']:
                    for h in i['transitions']:
                        all_list.append([j[0], h])
                all_possibility[i['name']] = all_list

        for i in all_possibility:
            for j in controlable_transitions:
                prevent_event_list = []
                if i['name'] == j['name']:
                    if i not in j:
                        prevent_event_list.append(i)
                prevent_event[i['name']] = prevent_event_list

        self.prevent_events = prevent_event

    def get_prevent_events(self):
        if self.prevent_events is None:
            self.set_prevent_events()
        return self.prevent_events

    @staticmethod
    def vetor_state(state):
        """"Cria uma string com os valores do vetor de state"""
        vetor_state = ""
        for i in range(len(state)):
            if i == 0:
                vetor_state += '1,'
            elif i == len(state) - 1:
                vetor_state += '0'
            else:
                vetor_state += '0,'
        return vetor_state

    def create_header(self):
        code = ""
        if self.language == "C":
            code = f"/{'*' * 50} \n"
            code += f"Data: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')} \n" \
                    f"Universidade do Estado de Santa Catarina \n" \
                    f"{'Anonymous'}\n" # TODO Arrumar isto
            code += f"{'*' * 50}\\ \n"
        return code

    def create_import(self):
        code = ""
        if self.language == "C":
            code += f"#include <wiringPi.h> \n\n"
        return code

    def start_function(self):
        code = "\n"
        if self.language == "C":
            code += f"int main(void){{ \n" \
                    f"    // When intialize wiring failed, print message to screen \n" \
                    f"    if(wiringPiSetup() == -1){{ \n" \
                    f'        println("setup wirginPi failed!"); \n' \
                    f"    return 1; \n    }} "
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
        code = ''
        var = self.format_var()
        for i in var:
            code += f"        bool {i} = 0;\n"
        return code

    def declare_state(self):
        code = ''
        if self.plant_states is None and self.supervisor_states is None:
            self.set_state()
        if self.language == "C":
            code += f"p_states[{len(self.plant_states)}] = {{" + self.vetor_state(self.plant_states) + "};\n"
            code += f"s_states[{len(self.supervisor_states)}] = {{" + self.vetor_state(self.supervisor_states) + "};\n"
        return code

    def declare_prevent_state(self):
        prevent_events = set()
        if self.prevent_events is None:
            self.set_prevent_events()
        for i in self.prevent_events:
            prevent_events.add(i[1])
        code = "        // Eventos desabilitados pelo supervisor \n"
        if self.prevent_events is None:
            self.get_prevent_events()
        for i in prevent_events:
            code += f"        bool D-EV{i[0]} = 0; \n"
        code += "\n"
        return code

    def declare_pin(self):
        code = "// Definição dos saida GPIO\n"
        j = 1
        for i in self.format_var():
            code += f"int {i}PIN = {j};\n"
            j += 1
        return code

    def read_inputs(self):
        """Inicia o código com a leitura das variáveis"""
        code = "        //Inicia a leitura das entradas \n"
        var = self.format_var()
        if self.language == "C":
            for i in range(len(sorted(self.all_events))):
                if int(var[i][-1]) % 2 == 0:
                    code += f"        {var[i]} = digitalRead({var[i]}PIN); \n"
        return code

    def format_prevent_events(self):
        condition1 = 'if'
        condition2 = 'elif'
        """Desabilitação dos Eventos Controláveis pelo supervisor"""
        code = "\n        // Desabilitação dos Eventos Controláveis pelo Supervisor\n"
        j = 0
        for i in self.prevent_events:
            if j == 0:
                code += f"        {condition1}(s_states[{i[0]}] == 1){{ \n"
            else:
                code += f"        {condition2}(s_states[{i[0]} == 1]){{ \n"
            code += f"            D_EV{i[1]} = 1\n" \
                    f"        }}"
        return code

    def update_state_nc(self, transitions, state_name):
        condition1 = 'if'
        condition2 = 'elif'
        """Atualização dos modelos da planta e do supervisor de acordo com os eventos não controláveis"""
        code = f"\n        //Atualiza os estados dos eventos não controláveis da {state_name}\n"
        transitions = list(transitions)
        j = 0
        if self.avalanche is None:
            self.check_avalanche()
        if self.language == "C":
            for i in range(len(transitions)):
                if int(transitions[i][1]) % 2 == 0 and transitions[i]:
                    if j == 0:
                        code += f"        {condition1}({state_name}[{transitions[i][0]}] == "
                    else:
                        code += f"        {condition2}({state_name}[{transitions[i][0]}] == "
                    code += f"1 && EV{transitions[i][1]} == HIGH){{\n" \
                            f"            {state_name}[{transitions[i][0]}] = 0;\n" \
                            f"            {state_name}[{transitions[i][2]}] = 1;\n" \
                            f"        }}\n"
                    j += 1
        return code

    def split_avalanche(self):
        for i in self.avalanche_list:
            if int(i[0]) < int(i[2]):
                self.crescent_avalanche.append(i)
            else:
                self.decrescent_avalanche.append(i)
        self.crescent_avalanche = sorted(self.crescent_avalanche, reverse=True)
        self.decrescent_avalanche = sorted(self.decrescent_avalanche)
        for i in self.supervisor_transitions:
            if i not in self.crescent_avalanche and i not in self.decrescent_avalanche:
                self.non_avalanche_list.append(i)

    def generate_controlable_events(self):
        condition1 = 'if'
        condition2 = 'elif'
        code = "\n        // Geração dos eventos Controláveis e atualização dos estados da planta\n"
        j = 0
        for i in self.plant_transitions:
            if int(i[1]) % 2 != 0:
                if j == 0:
                    code += f"        {condition1}(p_state{i[0]} = 1 && D_EV{i[0]} = 0){{\n"
                else:
                    code += f"        {condition2}(p_state{i[0]} = 1 && D_EV{i[0]} = 0){{\n"
                code += f"            p_state[{i[0]}] = 0;\n" \
                        f"            p_state[{i[2]}] = 1;\n" \
                        f"            EV{i[1]} = 1;\n" \
                        f"        }}\n"
                j += 1
        return code

    def update_supervisor_states(self):
        """Atualização dos Estados da planta pelos eventos controláveis"""
        condition1 = 'if'
        condition2 = 'elif'
        code = "\n        // Atualização dos Estados do Supervisor pelos Eventos Controláveis\n"
        j = 0
        for i in self.supervisor_transitions:
            if int(i[1]) % 2 != 0 and i[0] != i[2]:
                if j == 0:
                    code += f"        {condition1}(p_state{i[0]} = 1 && D_EV{i[0]} = 0){{\n"
                else:
                    code += f"        {condition2}(p_state{i[0]} = 1 && D_EV{i[0]} = 0){{\n"
                code += f"            p_state[{i[0]}] = 0;\n" \
                        f"            p_state[{i[2]}] = 1;\n"
        return code

    def setup_pin(self):
        """São Criado os Pinos de entrada e Saida"""
        code = "// Declara os GPIO Pin"
        if self.language == 'C':
            inp = 'INPUT'
            out = 'OUTPUT'
            for i in sorted(self.all_events):
                if int(i) % 2 == 0:
                    code += f'      pinMode(EV{i}Pin, {inp}); \n'
                else:
                    code += f'      pinMode(EV{i}Pin, {out}); \n'
        return code

    def write_outputs(self):
        code = "        // Escreve os eventos na saida\n"
        for i in self.all_events:
            if int(i) % 2 != 0:
                code += f"        if(EV{i} == 1){{\n" \
                        f"            EV{i}Pin =1;\n" \
                        f"        }}\n" \
                        f"        else{{\n" \
                        f"            EV{i}Pin = 0;\n" \
                        f"        }}\n"
        return code

    def create_loop(self):
        code = "\n"
        if self.language == "C":
            code = "\n    while(1){\n"
        return code

    @staticmethod
    def close_program():
        """Fecha """
        code = "    }\n" \
               "}"
        return code

    def corret_avalanche(self):
        code = ""
        self.check_avalanche()
        if self.avalanche is True:
            code += self.update_state_nc(self.non_avalanche_list, 's_state')
            code += self.update_state_nc(self.crescent_avalanche, 's_state')
            code += self.update_state_nc(self.decrescent_avalanche, 's_state')
        else:
            code += self.update_state_nc(self.supervisor_transitions, 's_state')
        return code

    def createcode_c(self):
        """ Chama a os métodos para a contrução do código"""
        # Declara o inicio do código
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
        code += self.update_state_nc(self.plants, 'p_state')
        code += self.corret_avalanche()
        code += self.format_prevent_events()
        code += self.generate_controlable_events()
        code += self.update_supervisor_states()
        code += self.write_outputs()
        code += self.close_program()
        return str(code)


