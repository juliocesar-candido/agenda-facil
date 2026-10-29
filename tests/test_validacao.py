"""Testes das funcoes de validacao de entradas."""

import unittest
from datetime import date

from agenda_facil.excecoes import EntradaInvalidaError
from agenda_facil.validacao import (
    criar_atendimento,
    validar_data,
    validar_duracao,
    validar_hora_inicio,
    validar_termino_no_expediente,
    validar_texto_obrigatorio,
)


class ValidarDataTest(unittest.TestCase):
    def test_data_valida(self):
        self.assertEqual(validar_data("2026-10-05"), date(2026, 10, 5))

    def test_formatos_invalidos(self):
        for valor in ["05/10/2026", "2026-1-5", "20261005", "", "hoje", None, 20261005]:
            with self.subTest(valor=valor):
                with self.assertRaises(EntradaInvalidaError):
                    validar_data(valor)

    def test_data_inexistente_no_calendario(self):
        with self.assertRaises(EntradaInvalidaError):
            validar_data("2026-02-30")

    def test_digitos_nao_ascii_sao_rejeitados(self):
        with self.assertRaises(EntradaInvalidaError):
            validar_data("٢٠٢٦-١٠-٠٥")


class ValidarHoraTest(unittest.TestCase):
    def test_limites_do_expediente(self):
        self.assertEqual(validar_hora_inicio(8), 8)
        self.assertEqual(validar_hora_inicio(17), 17)

    def test_fora_do_expediente_ou_tipo_errado(self):
        for valor in [7, 18, 20, -1, 9.0, "9", None, True]:
            with self.subTest(valor=valor):
                with self.assertRaises(EntradaInvalidaError):
                    validar_hora_inicio(valor)


class ValidarDuracaoTest(unittest.TestCase):
    def test_duracoes_validas(self):
        for valor in [15, 30, 45, 60, 120]:
            with self.subTest(valor=valor):
                self.assertEqual(validar_duracao(valor), valor)

    def test_duracoes_invalidas(self):
        for valor in [0, 10, 14, 20, 135, 150, -15, 30.0, "30", None, True]:
            with self.subTest(valor=valor):
                with self.assertRaises(EntradaInvalidaError):
                    validar_duracao(valor)


class ValidarTerminoTest(unittest.TestCase):
    def test_termina_exatamente_as_18h(self):
        validar_termino_no_expediente(17, 60)

    def test_passa_das_18h(self):
        with self.assertRaises(EntradaInvalidaError):
            validar_termino_no_expediente(17, 75)


class ValidarTextoTest(unittest.TestCase):
    def test_remove_espacos_das_pontas(self):
        self.assertEqual(validar_texto_obrigatorio("  Ana ", "paciente"), "Ana")

    def test_vazio_ou_nao_texto(self):
        for valor in ["", "   ", None, 5]:
            with self.subTest(valor=valor):
                with self.assertRaises(EntradaInvalidaError):
                    validar_texto_obrigatorio(valor, "paciente")

    def test_mensagem_cita_o_campo_e_o_valor(self):
        with self.assertRaises(EntradaInvalidaError) as ctx:
            validar_texto_obrigatorio(None, "paciente")
        self.assertIn("paciente", str(ctx.exception))
        self.assertIn("None", str(ctx.exception))


class CriarAtendimentoTest(unittest.TestCase):
    def test_cria_atendimento_valido(self):
        a = criar_atendimento("Ana", "Dr. Silva", "2026-10-05", 9, 30)
        self.assertEqual(a.data, date(2026, 10, 5))
        self.assertEqual(a.status, "MARCADO")

    def test_entrada_invalida_propaga_como_value_error(self):
        with self.assertRaises(ValueError):
            criar_atendimento("Ana", "Dr. Silva", "2026-10-05", 20, 30)


if __name__ == "__main__":
    unittest.main()