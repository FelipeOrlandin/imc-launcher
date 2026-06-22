"""Testes para o dataclass ResultadoIMC."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.modelos import ResultadoIMC


class TestResultadoIMC(unittest.TestCase):

    def setUp(self):
        self.resultado = ResultadoIMC(
            nome="Joao",
            idade=25,
            altura=1.75,
            peso=70,
            imc=22.86,
            categoria="no peso ideal",
            classificacao="Peso normal",
            ano_nascimento=2001,
        )

    def test_campos_armazenados(self):
        self.assertEqual(self.resultado.nome, "Joao")
        self.assertEqual(self.resultado.idade, 25)
        self.assertEqual(self.resultado.altura, 1.75)
        self.assertEqual(self.resultado.peso, 70)
        self.assertEqual(self.resultado.ano_nascimento, 2001)

    def test_formatar_contem_nome(self):
        texto = self.resultado.formatar()
        self.assertIn("Joao", texto)

    def test_formatar_contem_imc(self):
        texto = self.resultado.formatar()
        self.assertIn("22.86", texto)

    def test_formatar_contem_classificacao(self):
        texto = self.resultado.formatar()
        self.assertIn("Peso normal", texto)

    def test_formatar_contem_ano(self):
        texto = self.resultado.formatar()
        self.assertIn("2001", texto)

    def test_formatar_separadores(self):
        texto = self.resultado.formatar()
        self.assertIn("=", texto)


if __name__ == '__main__':
    unittest.main()