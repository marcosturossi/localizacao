from datetime import datetime


class Supervisor:
    def __init__(self, language, **kwargs):
        self.plant_name = kwargs['plant']['name']
        self.supervisor_name = kwargs['supervisor']['name']
        self.plant_transitions = kwargs['plant']['transitions']
        self.supervisor_transitions = kwargs['supervisor']['transitions']
        self.plant_marked = kwargs['plant']['marker']
        self.supervisor_marked = kwargs['supervisor']['marker']
        self.language = language
        self.plant_events = None
        self.supervisor_events = None
        self.all_events = None
        self.plant_states = None
        self.supervisor_states = None
        self.all_states = None

    def set_events(self):
        """Adiciona os eventos aos atributos"""
        self.plant_events = set()
        self.supervisor_events = set()
        self.all_events = set()
        for i in self.plant_transitions:
            self.plant_events.add(i[1])
            self.all_events.add(i[1])
        for i in self.supervisor_transitions:
            self.supervisor_events.add(i[1])
            self.all_events.add(i[1])

    def get_events(self):
        """Recupera os eventos"""
        if self.plant_events is None and self.supervisor_events is None:
            self.set_events()
        return self.plant_events, self.supervisor_events

    def set_state(self):
        self.plant_states = set()
        self.supervisor_states = set()
        self.all_states = set()
        for i in self.plant_transitions:
            self.plant_states.add(i[0])
            self.plant_states.add(i[2])
            self.all_states.add(i[0])
            self.all_states.add(i[1])
        for i in self.supervisor_transitions:
            self.supervisor_states.add(i[0])
            self.supervisor_states.add(i[2])
            self.all_states.add(i[0])
            self.all_states.add(i[1])

    def get_states(self):
        if self.plant_states is None and self.supervisor_states is None:
            self.set_state()
        return self.plant_states, self.supervisor_states

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
                    f"{self.name()}\n"
            code += f"{'*' * 50}\\ \n"
        return code

    def create_import(self, bibliotecas=None):
        code = ""
        if self.language == "C":
            code += f"#include <wiringPi.h> \n\n"
        return code

    def start_function(self):
        code = "\n"
        if self.language == "C":
            code += f"int main(void){{ \n" \
                    f"// When intialize wiring failed, print message to screen \n" \
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
            code += f"bool {i};\n"
        return code

    def declare_state(self):
        code = ''
        if self.plant_states is None and self.supervisor_states is None:
            self.set_state()
        if self.language == "C":
            code += f"p_states[{len(self.plant_states)}] = {{" + self.vetor_state(self.plant_states) + "};\n"
            code += f"s_states[{len(self.supervisor_states)}] = {{" + self.vetor_state(self.supervisor_states) + "};\n"
        return code

    def declare_pin(self):
        code = ""
        j = 1
        for i in self.format_var():
            code += f"int {i}PIN = {j};\n"
            j += 1
        return code

    def read_inputs(self):
        """Inicia o código com a leitura das variáveis"""
        code = ""
        var = self.format_var()
        if self.language == "C":
            for i in range(len(sorted(self.all_events))):
                if int(var[i][-1]) % 2 == 0:
                    code += f"      {var[i]} = digitalRead({var[i]}PIN); \n"
        return code

    def update_state_nc(self, transitions, state_name):
        condition1 = 'if'
        condition2 = 'elif'
        """Atualização dos modelos da planta e do supervisor de acordo com os eventos não controláveis"""
        code = f"\n      //Atualiza os estados dos eventos não controláveis da {state_name}\n"
        transitions = list(transitions)
        j = 0
        if self.language == "C":
            for i in range(len(transitions)):
                if int(transitions[i][1]) % 2 == 0:  # Se for não controlável
                    if j == 0:
                        code += f"      {condition1}({state_name}[{transitions[i][0]}] == "
                    else:
                        code += f"      {condition2}({state_name}[{transitions[i][0]}] == "
                    code += f"1 and EV{transitions[i][1]} == HIGH){{\n" \
                    f"          {state_name}[{transitions[i][0]}] = 0;\n" \
                    f"          {state_name}[{transitions[i][2]}] = 1;\n" \
                    f"          }}\n"
                    j +=1
        return code

    def create_loop(self):
        code = "\n"
        if self.language == "C":
            code = "\n    while(1){\n" \
                   "\n    //Inicia a leitura das entradas \n"
        return code

    def name(self):
        return f'{self.plant_name}-{self.supervisor_name}'

    def __str__(self):
        return f'{self.plant_name}-{self.supervisor_name}'


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
        """Set se os pinos sao entrada ou saida"""
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
        code = self.create_header()
        code += self.create_import()
        code += self.declare_pin()
        code += self.declare_state()
        code += self.declared_var()
        code += self.start_function()
        code += self.setup_pin()

        # Inicia a lógica de Controle
        code += self.create_loop()
        code += self.read_inputs()
        code += self.update_state_nc(self.plant_transitions, 'p_state')
        code += self.update_state_nc(self.supervisor_transitions, 's_state')
        return str(code)
