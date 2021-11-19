from django.test import TestCase
from .language.c import C
from .supervisors.supervisor import Supervisor


class TesteC(TestCase):
    def setUp(self):
        self.c = C()
        self.supervisor = Supervisor(C()) # Test Supervisor Modular Local

    def testa_languague_sintax(self):
        function_exemple ='int main(void){\n    println("Hello World");\n}\n'
        self.assertEqual(self.c.o_declare_var('int', 'main', 3), "int main = 3;\n")
        self.assertEqual(self.c.o_declare_function('int', 'main', 'println("Hello World")'), function_exemple)

    def testa_modular_local(self):
        pass
