import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.calculadora import calcular_imc


class TestCalculadoraIMC(unittest.TestCase):
    """Testes para a calculadora de IMC padrao OMS."""
    
    def test_peso_normal(self):
        resultado = calcular_imc("Teste", 25, 1.75, 70, 2026)
        self.assertEqual(resultado.categoria, "no peso ideal")
        self.assertEqual(resultado.classificacao, "Peso normal")
        self.assertAlmostEqual(resultado.imc, 22.86, places=2)
    
    def test_abaixo_peso(self):
        resultado = calcular_imc("Teste", 20, 1.80, 55, 2026)
        self.assertEqual(resultado.categoria, "abaixo do peso")
        self.assertEqual(resultado.classificacao, "Abaixo do peso")
    
    def test_sobrepeso(self):
        resultado = calcular_imc("Teste", 30, 1.70, 85, 2026)
        self.assertEqual(resultado.categoria, "com sobrepeso")
        self.assertEqual(resultado.classificacao, "Sobrepeso")
    
    def test_obesidade(self):
        resultado = calcular_imc("Teste", 35, 1.65, 100, 2026)
        self.assertEqual(resultado.categoria, "com obesidade")
        self.assertEqual(resultado.classificacao, "Obesidade")
    
    def test_validacao_altura_baixa(self):
        with self.assertRaises(ValueError):
            calcular_imc("Teste", 25, 0.3, 70, 2026)
    
    def test_validacao_altura_alta(self):
        with self.assertRaises(ValueError):
            calcular_imc("Teste", 25, 3.0, 70, 2026)
    
    def test_validacao_peso_baixo(self):
        with self.assertRaises(ValueError):
            calcular_imc("Teste", 25, 1.75, 10, 2026)
    
    def test_validacao_peso_alto(self):
        with self.assertRaises(ValueError):
            calcular_imc("Teste", 25, 1.75, 400, 2026)
    
    def test_validacao_idade(self):
        with self.assertRaises(ValueError):
            calcular_imc("Teste", 0, 1.75, 70, 2026)
    
    def test_ano_nascimento(self):
        resultado = calcular_imc("Teste", 24, 1.84, 70, 2026)
        self.assertEqual(resultado.ano_nascimento, 2002)
    
    def test_formatar_saida(self):
        resultado = calcular_imc("Joao", 25, 1.75, 70, 2026)
        texto = resultado.formatar()
        self.assertIn("Joao", texto)
        self.assertIn("2001", texto)
        self.assertIn("22.86", texto)


if __name__ == '__main__':
    unittest.main()