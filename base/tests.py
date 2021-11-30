from django.test import TestCase
from .language.c import C
from .supervisors.supervisor import Supervisor, Plant, Automato
from .supervisors.modular_local import ModularLocal
from .supervisors.localization import SupervisorLocalizado
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
        with open('base/data/loc1.ads', 'rb') as loc1:
            self.loc1 = clean_data(loc1.readlines())
        with open('base/data/loc2.ads', 'rb') as loc2:
            self.loc2 = clean_data(loc2.readlines())
        # with open('base/data/loc3.ads', 'rb') as loc3:
        #     self.loc3 = clean_data(loc3.readlines())

    def testa_automato(self):
        a1 = Automato(self.m1)
        a1.set_events()
        self.assertEqual(a1.get_events(), {'1', '2'})
        a1.set_states()
        self.assertEqual(a1.get_states(), {'0', '1'})
        a1.set_named_events()
        self.assertEqual(a1.named_events, {'1': 'EV1', '2': 'EV2'})
        a1._split_transitions()
        self.assertEqual(a1.controlable, [['0', '1', '1']])
        self.assertEqual(a1.non_controlable, [['1', '2', '0']])
        self.assertEqual(a1.get_name(), 'M1')
        self.assertEqual(a1.get_transitions(), [['0', '1', '1'], ['1', '2', '0']])

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
        m1 = Plant(self.m1)
        m2 = Plant(self.m2)
        tu = Plant(self.tu)
        sr1 = Supervisor(self.sr1)
        sr2 = Supervisor(self.sr2)
        sr3 = Supervisor(self.sr3)
        ml = ModularLocal(C())
        ml.set_data(tu)
        ml.set_data(sr3)
        self.assertListEqual(ml.get_controlable(), [['0', '1', '0'],
                                                    ['1', '1', '1'],
                                                    ['1', '5', '1'],
                                                    ['2', '1', '2'],
                                                    ['2', '5', '2'],
                                                    ['3', '5', '3']])

        self.assertListEqual(ml.get_non_controlable(), [['1', '6', '0'],
                                                        ['2', '6', '1'],
                                                        ['3', '6', '2'],
                                                        ['2', '2', '3'],
                                                        ['1', '2', '2'],
                                                        ['0', '2', '1']])
        self.assertEqual(ml.get_non_controlable_events(), {'2', '6'})
        self.assertEqual(ml.get_controlable_events(), {'1', '5'})

    def testa_localizacao(self):
        m2 = Plant(self.m2)
        loc2 = Supervisor(self.loc2)
        sup_loc = SupervisorLocalizado(C())
        sup_loc.set_data(m2)
        sup_loc.set_data(loc2)
        self.assertEqual(sup_loc.get_non_plant_events(), ['2', '5', '8'])
        self.assertEqual(sup_loc.get_non_controlable_events(), {'2', '4', '5', '8'})
