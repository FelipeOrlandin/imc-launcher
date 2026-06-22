"""Testes para validadores."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.validators import validar_nome, validar_decimal


class TestValidarNome(unittest.TestCase):

    def test_nome_valido(self):
        self.assertTrue(validar_nome("Joao Silva"))
        self.assertTrue(validar_nome("Maria"))
        self.assertTrue(validar_nome("Jose da Silva"))

    def test_nome_com_acentos(self):
        self.assertTrue(validar_nome("Jose"))
        self.assertTrue(validar_nome("Macã"))
        self.assertTrue(validar_nome("Ana Beatriz"))

    def test_nome_com_espacos(self):
        self.assertTrue(validar_nome("Joao da Silva"))

    def test_nome_muito_longo(self):
        self.assertFalse(validar_nome("A" * 51))

    def test_nome_com_numeros(self):
        self.assertFalse(validar_nome("Joao123"))

    def test_nome_vazio(self):
        self.assertTrue(validar_nome(""))


class TestValidarDecimal(unittest.TestCase):

    def test_decimal_valido(self):
        self.assertTrue(validar_decimal("1.75"))
        self.assertTrue(validar_decimal("70"))
        self.assertTrue(validar_decimal("70.5"))

    def test_decimal_vazio(self):
        self.assertTrue(validar_decimal(""))

    def test_decimal_ponto_sozinho(self):
        self.assertFalse(validar_decimal("."))
        self.assertFalse(validar_decimal(","))

    def test_decimal_virgula(self):
        self.assertTrue(validar_decimal("1,75"))

    def test_decimal_multiplos_pontos(self):
        self.assertFalse(validar_decimal("1.2.3"))

    def test_decimal_letras(self):
        self.assertFalse(validar_decimal("abc"))


if __name__ == '__main__':
    unittest.main()