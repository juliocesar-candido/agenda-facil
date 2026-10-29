"""Regra de ouro: a demonstracao deve imprimir exatamente a saida do codigo-base."""

import contextlib
import io
import unittest

from agenda_facil.demonstracao import executar_demonstracao

SAIDA_ESPERADA = (
    "Atendimento marcado para Ana\n"
    "Horario ocupado\n"
    "Atendimento marcado para Carla\n"
    "Remarcado\n"
    "14 Carla Dra. Souza MARCADO\n"
)


class DemonstracaoTest(unittest.TestCase):
    def test_saida_identica_a_do_codigo_base(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            executar_demonstracao()
        self.assertEqual(buffer.getvalue(), SAIDA_ESPERADA)


if __name__ == "__main__":
    unittest.main()