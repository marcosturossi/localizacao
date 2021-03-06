
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

    def set_named_events(self, events=None):
        if events:
            named_events = {}
            for i in events:
                named_events[str(i)] = f"EV{i}"
            return named_events
        if not self.events:
            self.set_events()
        for i in self.events:
            self.named_events[str(i)] = f"EV{i}"

    def _split_transitions(self):
        self.non_controlable = []
        self.controlable = []
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

    def get_named_events(self, events=None):
        if events:
            return self.set_named_events(events)
        if not self.named_events:
            self.set_named_events()
        return self.named_events


class Plant(Automato):
    def get_correlated_events(self):
        correlated_events = []
        non_correlated_events = []
        controlable = self.get_controlable()
        non_controlable = self.get_non_controlable()
        for j in controlable:
            for k in non_controlable:
                if j[0] == k[2] and j[2] == k[0]:
                    correlated_events.append([j[1], k[1]])
                else:
                    non_correlated_events.append(j[1])
                    non_correlated_events.append(k[1])
        return self._named_correlated(correlated_events, non_correlated_events)

    def _named_correlated(self, correlated, non_correlated):
        named_correlated, named_non_correlated = [], []
        for i in correlated:
            named_correlated.append(self.get_named_events(i))
        for j in non_correlated:
            named_non_correlated.append((self.get_named_events(j)))
        return named_correlated, named_non_correlated


class Supervisor(Automato):
    def __init__(self, data):
        super().__init__(data)
        self.avalanche = None
        self.avalanche_checked = False
        self.avalanche_list = []
        self.non_avalanche_list = []
        self.prevent_events = []
        self.choice_problem = None

    def get_transitions(self):
        if not self.avalanche_checked:
            self.check_avalanche()
        return super().get_transitions()

    def get_controlable(self):
        if not self.avalanche_checked:
            self.check_avalanche()
        return super().get_controlable()

    def get_non_controlable(self):
        if not self.avalanche_checked:
            self.check_avalanche()
        return super().get_non_controlable()

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
        for i in self.get_controlable():
            new_transitions.append([i[0], i[1]])
        return new_transitions

    def set_prevent_events(self):
        controlable = self._clone_copy_transistions()
        for i in self._get_all_possibility():
            if i not in controlable:
                self.prevent_events.append(i)

    def get_prevent_events(self):
        if not self.prevent_events:
            self.set_prevent_events()
        return sorted(self.prevent_events)

    def check_avalanche(self):
        trans = self.transitions
        self.avalanche_list = []
        self.non_avalanche_list = []
        for i in range(len(trans)):
            for j in range(1, len(trans)):
                if trans[i][1] == trans[j][1] and i != j:
                    if trans[i][0] == trans[j][2]:
                        self.avalanche = True
                        self.avalanche_list.append(trans[i])
                        self.avalanche_list.append(trans[j])
        if self.avalanche:
            self._solve_avalanche()
        self.avalanche_checked = True

    def _solve_avalanche(self):
        crescent = []
        decrescent = []
        new_list = []
        duplicated = []
        for i in self.avalanche_list:
            if i[0] > i[2] and i not in duplicated:
                duplicated.append(i)
                crescent.append(i)
            elif i[2] > i[0] and i not in duplicated:
                duplicated.append(i)
                decrescent.append(i)
        crescent = sorted(crescent)
        decrescent = sorted(decrescent, reverse=True)
        for i in crescent:
            new_list.append(i)
        for j in decrescent:
            new_list.append(j)
        for k in new_list:
            self.transitions.remove(k)
        self.transitions.extend(new_list)
        self._split_transitions()

    def remove_controlable(self, transitions):
        """Utilizado para Localização de Supervisor"""
        self.controlable.remove(transitions)
        self.non_controlable.append(transitions)

    def check_choice_problem(self):
        pass
