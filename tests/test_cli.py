"""Testes para o CLI."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestCLI(unittest.TestCase):

    def _run_cli(self, args):
        """Roda o CLI diretamente e retorna (returncode, output)."""
        original_argv = sys.argv
        try:
            sys.argv = ["cli"] + args
            from cli.main import main
            import io
            from contextlib import redirect_stdout
            f = io.StringIO()
            try:
                with redirect_stdout(f):
                    main()
                return 0, f.getvalue()
            except SystemExit as e:
                return e.code, f.getvalue()
        finally:
            sys.argv = original_argv

    def test_uso_correto(self):
        code, output = self._run_cli(["Joao", "25", "1.75", "70", "2026"])
        self.assertEqual(code, 0)
        self.assertIn("Joao", output)
        self.assertIn("22.86", output)

    def test_argumentos_insuficientes(self):
        code, output = self._run_cli([])
        self.assertNotEqual(code, 0)

    def test_altura_invalida(self):
        code, output = self._run_cli(["Joao", "25", "3.0", "70", "2026"])
        self.assertNotEqual(code, 0)
        self.assertIn("Altura", output)

    def test_peso_invalido(self):
        code, output = self._run_cli(["Joao", "25", "1.75", "10", "2026"])
        self.assertNotEqual(code, 0)
        self.assertIn("Peso", output)

    def test_idade_invalida(self):
        code, output = self._run_cli(["Joao", "200", "1.75", "70", "2026"])
        self.assertNotEqual(code, 0)
        self.assertIn("Idade", output)


if __name__ == '__main__':
    unittest.main()