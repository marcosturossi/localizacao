
class Automato:
    def __init__(self, data):
        self.name = data['name']
        self.transitions = data['transitions']
        self.events = set()  # Set de Eventos
        self.states = set()  # Set de Estados
        self.non_controlable = []  # Transições Não Controláveis
        self.controlable = []  # Transições Controláveis
        self.named_events = {}  # Organiza os Eventos em nomes

    def set_events(self):
        for i in self.transitions:
            self.events.add(i[1])

    def set_states(self):
        for i in self.transitions:
            self.states.add(i[0])
            self.states.add(i[2])

    def set_named_events(self):
        if not self.events:
            self.set_events()
        for i in self.events:
            self.named_events[str(i)] = f"EV{i}"

    def _split_transitions(self):
        for i in self.transitions:
            if int(i[1]) % 2 == 0:
                self.non_controlable.append(i)
            else:
                self.controlable.append(i)

    def get_name(self):
        return self.name

    def get_transitions(self):
        return self.transitions

    def get_controlable(self):
        if not self.controlable:
            self._split_transitions()
        return self.controlable

    def get_non_controlable(self):
        if not self.non_controlable:
            self._split_transitions()
        return self.non_controlable

    def get_events(self):
        if not self.events:
            self.set_events()
        return self.events

    def get_states(self):
        if not self.states:
            self.set_states()
        return self.states

    def get_named_events(self):
        if not self.named_events:
            self.set_named_events()
        return self.named_events


class Plant(Automato):
    pass


class Supervisor(Automato):
    def __init__(self, data):
        super().__init__(data)
        self.avalanche = None
        self.avalanche_solved = False
        self.avalanche_list = []
        self.prevent_events = []
        self.choice_problem = None

    def _get_all_possibility(self):
        """Função que cria todas as possobilidades de saida de eventos
        auxilia verificação de eventos impedidos pelo supervisor"""
        all_possibility = []
        states = self.get_states()
        events = self.get_events()
        for i in states:
            for j in events:
                if int(j) % 2 != 0:
                    all_possibility.append([i, j])
        return all_possibility

    def _clone_copy_transistions(self):
        """Nova lista de transições com apenas o estado de saida
        e o evento"""
        new_transitions = []
        controlable = self.get_controlable()
        for i in controlable:
            new_transitions.append([i[0], [1]])
        return new_transitions

    def set_prevent_events(self):
        controlable = self._clone_copy_transistions()
        for i in self._get_all_possibility():
            if i not in controlable:
                self.prevent_events.append(i)

    def get_prevent_events(self):
        if not self.prevent_events:
            self.set_prevent_events()
        return self.prevent_events

    def _clean_avalalanche_list(self):
        for i in self.avalanche_list:
            if self.avalanche_list.count(i) > 1:
                self.avalanche_list.remove(i)

    def _solve_avalanche_list(self):
        crescent = []
        decrescent = []
        non_avalanche = []
        for i in self.avalanche_list:
            if int(i[0]) > int(i[2]):
                crescent.append(i)
            else:
                decrescent.append(i)
        crescent = sorted(crescent, reverse=True)
        decrescent = sorted(decrescent)
        for i in self.transitions:
            if i not in crescent and i not in decrescent:
                non_avalanche.append(i)
        self.avalanche_list = []
        for i in crescent:
            self.avalanche_list.append(i)
        for i in decrescent:
            self.avalanche_list.append(i)
        for i in non_avalanche:
            self.avalanche_list.append(i)

    def check_avalanche(self):
        trans = self.get_transitions()
        for i in range(len(trans)):
            for j in range(1, len(trans)):
                if trans[i][1] == trans[j][1] and i != j:
                    if trans[i][2] == trans[j][0]:
                        self.avalanche_list.append(trans[i])
                        self.avalanche_list.append(trans[j])
                        self.avalanche = True
        if self.avalanche:
            self._clean_avalalanche_list()
            self._solve_avalanche_list()
            self.avalanche_solved = True

    def check_choice_problem(self):
        pass
