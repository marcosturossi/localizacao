import re


def clean_data(data):
    """Retira os textos de comentário, e os espaços devolvendo o dados em uma lista"""
    new_data = []
    for line in data:
        if type(line) != str:
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


