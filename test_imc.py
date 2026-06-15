import unittest
from imc_core import calcular_imc

class TestIMC(unittest.TestCase):
    
    def test_abaixo_do_peso(self):
        resultado = calcular_imc("João", 25, 1.80, 60, 2026)
        self.assertIn("abaixo do peso", resultado)

    def test_peso_ideal(self):
        resultado = calcular_imc("Felipe", 23, 1.83, 70, 2026)
        self.assertIn("no peso ideal", resultado)

    def test_sobrepeso(self):
        resultado = calcular_imc("maria", 40, 1.60, 100, 2026)
        self.assertIn("com sobrepeso", resultado)

    def test_ano_nascimento(self):
        resultado = calcular_imc("Felipe", 24, 1.84, 70, 2026)
        self.assertIn("nasceu em 2002", resultado)

if __name__ == '__main__':
    unittest.main()