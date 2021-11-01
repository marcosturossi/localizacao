import re


def clean_data(data):
    """Retira os textos de comentário, e os espaços devolvendo o dados em uma lista"""
    new_data = []
    for line in data:
        line = line.decode().replace('\r\n', '')
        if re.search(r'^[a-zA-z0-9]', line):
            line = re.sub(r'\s+', ' ', line)
            new_data.append(line)
    return list2dict(new_data)


def list2dict(data):
    """Organiza os dados em um dicionário para facilidar o trabalho"""
    dict_data = {'name': data[0], 'size': data.index('State size (State set will be (0,1....,size-1)):') + 1}
    transitions_list = data[data.index('Transitions:') + 1:]
    markerstate_list = data[data.index('Marker states:') + 1: data.index('Vocal states:')]
    vocal_state_list = data[data.index('Vocal states:') + 1: data.index('Transitions:')]
    dict_data['transitions'] = transitions_array(transitions_list)
    dict_data['marker'] = markerstate_list
    dict_data['vocal'] = vocal_state_list
    return dict_data


def transitions_array(data_list):
    """Transforma as strings em listas de transições"""
    array_transitions = []
    for transitions in data_list:
        transitions = transitions.split(' ')
        transitions.pop(3)
        array_transitions.append(transitions)
    return array_transitions


def check_avanlanche(transitions):
    """Eventos Controláveis somente são impares, e eventos não controláveis são pares"""
    transitions = transitions['transitions']
    lista_avalance = []
    avalanche = False
    for i in range(len(transitions)):
        for j in range(1, len(transitions)):
            if transitions[i][1] == transitions[j][1] and i != j:  # Verifica se os eventos são iguais
                if transitions[i][2] == transitions[j][0]:
                    lista_avalance.append(transitions[i])
                    lista_avalance.append(transitions[j])
                    avalanche = True
    return lista_avalance, avalanche


def check_choice(transitions):
    """Verifica se existe o problema de escolha no supervisor"""
    transitions = transitions['transitions']
    choice_list = []
    chooseable = False
    for i in range(len(transitions)):
        for j in range(1, len(transitions)):
            if transitions[i][1] == transitions[j][1] and i != j and int(transitions[i][1]) % 2 != 0 and transitions[i][0] == transitions[j][0]:
                choice_list.append(transitions[i])
                choice_list.append(transitions[j])
                chooseable = True
    return choice_list, chooseable


def set_starting_variables(data):
    """Separa os eventos não controláveis, controláveis, e estados"""
    transitions = data['transitions']
    set_state = set()
    set_non_controlable = set()
    set_controlable = set()
    for item in transitions:
        set_state.add(item[0])
        set_state.add(item[2])
        if int(item[1]) % 2 == 0:
            set_non_controlable.add(item[1])
        else:
            set_controlable.add(item[1])
    return set_state, set_non_controlable, set_controlable


def declarete_variables(set_state, set_non_controlable, set_controlable):
    initial = f'VAR \n' \
              f'  // Vetor de Estados\n' \
              f'  states: ARRAY[{len(set_state)}] OF BOOL := ['
    for i in range(len(set_state)):
        if i == len(set_state)-1:
            initial += 'FALSE];\n'
        elif i == 0:
            initial += 'TRUE,'
        else:
            initial += 'FALSE,'
    initial += f'  // Eventos não Controláveis\n'
    for i in set_non_controlable:
        initial += f'  e{i} := BOOL;\n'
    initial += f'  // Eventos Controláveis\n'
    for i in set_controlable:
        initial += f'  e{i} := BOOL;\n'
    initial += 'END_VAR'
    return initial
