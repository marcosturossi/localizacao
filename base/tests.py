from django.test import TestCase
from .language.c import C


class TesteC(TestCase):
    def setUp(self):
        self.c = C()

    def testa_declara_variavel(self):
        function_exemple ='int main(void){\n    println("Hello World");\n}\n'
        self.assertEqual(self.c.o_declare_var('int', 'main', 3), "int main = 3;\n")
        self.assertEqual(self.c.o_declare_function('int', 'main', 'println("Hello World")'), function_exemple)
