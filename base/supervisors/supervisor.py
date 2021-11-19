
class Automato:
    def __init__(self, transitions):
        self.name = transitions['name']
        self.transitions = transitions
        self.events = set()
        self.non_controlable = []  # Transições Não Controláveis
        self.controlable = []  # Transições Controláveis
        self.named_events = {}  # Organiza os Eventos em nomes

    def set_events(self):
        for i in self.transitions:
            self.events.add(i[1])

    def set_named_events(self):
        for i in self.events:
            self.named_events[i](f"EV{i}")

    def split_transitions(self):
        for i in self.transitions:
            if int(i[1]) % 2 == 0:
                self.non_controlable.append(i)
            else:
                self.controlable.append(i)


class Plant(Automato):
    pass


class Supervisor(Automato):
    def __init__(self, transitions):
        super().__init__(transitions)
        self.avalanche = None
        self.avalanche = []
        self.prevent_events = []

    def get_prevent_events(self):
        pass

    def check_avalanche(self):
        pass

    def check_choice_problem(self):
        pass
