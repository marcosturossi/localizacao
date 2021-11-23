from django.test import TestCase
from .language.c import C
from .supervisors.supervisor import Supervisor, Plant, Automato
from .reader import clean_data


class Teste(TestCase):
    def setUp(self):
        with open('base/data/m1.ads', 'rb') as m1:
            self.m1 = clean_data(m1.readlines())
        with open('base/data/m2.ads', 'rb') as m2:
            self.m2 = clean_data(m2.readlines())
        with open('base/data/tu.ads', 'rb') as tu:
            self.tu = clean_data(tu.readlines())
        with open('base/data/sr1.ads', 'rb') as sr1:
            self.sr1 = clean_data(sr1.readlines())
        with open('base/data/sr2.ads', 'rb') as sr2:
            self.sr2 = clean_data(sr2.readlines())
        with open('base/data/sr3.ads', 'rb') as sr3:
            self.sr3 = clean_data(sr3.readlines())

    def testa_automato(self):
        a1 = Automato(self.m1)
        a1.set_events()
        self.assertEqual(a1.get_events(), {'1', '2'})
        a1.set_states()
        self.assertEqual(a1.get_states(), {'0', '1'})
        a1.set_named_events()
        self.assertEqual(a1.named_events,  {'1': 'EV1', '2': 'EV2'})
        a1._split_transitions()
        self.assertEqual(a1.controlable, [['0', '1', '1']])
        self.assertEqual(a1.non_controlable, [['1', '2', '0']])
        self.assertEqual(a1.get_name(), 'M1')
        self.assertEqual(a1.get_transitions(), [['0', '1', '1'],['1', '2', '0']])

    def testa_planta(self):
        p1 = Plant(self.m1)
        named_events = ([{'1': 'EV1', '2': 'EV2'}], [])
        self.assertEqual(p1.get_correlated_events(), named_events)

    def testa_supervisor(self):
        s2 = Supervisor(self.sr2)
        transitions = [['0', '3', '0'], ['0', '4', '1'], ['1', '5', '0']]
        controlable = [['0', '3', '0'], ['1', '5', '0']]
        non_controlable = [['0', '4', '1']]
        prevent_events = [['0', '5'], ['1', '3']]
        self.assertEqual(len(s2.get_transitions()), 3)
        self.assertEqual(s2.get_transitions(), transitions)
        self.assertEqual(s2.get_controlable(), controlable)
        self.assertEqual(s2.get_non_controlable(), non_controlable)
        s2.check_avalanche()
        self.assertEqual(s2.avalanche_checked, True)
        self.assertEqual(s2.get_prevent_events(), prevent_events)
        # testa se o avalanche foi resolvido
        s3 = Supervisor(self.sr3)
        self.assertEqual(s3.avalanche_checked, False)
        self.assertEqual(len(s3.get_transitions()), 12)
        self.assertEqual(len(s3.transitions), len(s3.get_transitions()))
        s3.check_avalanche()
        self.assertEqual(s3.avalanche_checked, True)
        s1 = Supervisor(self.sr1)
        self.assertEqual(s1.avalanche_checked, False)
        s1.check_avalanche()
        self.assertEqual(len(s1.transitions), len(s1.get_transitions()))
        self.assertEqual(len(s1.get_transitions()), 30)
        self.assertGreater(len(s1.get_transitions()), len(s1.get_controlable()))
        self.assertGreater(len(s1.get_transitions()), len(s1.get_non_controlable()))
        self.assertEqual(s1.avalanche_checked, True)

    def testa_modular_local(self):
        pass

