"""Testes das regras de agendamento (marcar, remarcar e listar)."""

import unittest

from agenda_facil import (
    Agenda,
    AtendimentoNaoEncontradoError,
    ConflitoHorarioError,
    EntradaInvalidaError,
)


class MarcarTest(unittest.TestCase):
    def setUp(self):
        self.agenda = Agenda()

    def test_marca_e_devolve_o_atendimento(self):
        a = self.agenda.marcar("Ana", "Dr. Silva", "2026-10-05", 9, 30)
        self.assertEqual(a.paciente, "Ana")
        self.assertEqual(self.agenda.listar_por_data("2026-10-05"), [a])

    def test_conflito_mesmo_profissional_dia_e_hora(self):
        self.agenda.marcar("Ana", "Dr. Silva", "2026-10-05", 9, 30)
        with self.assertRaises(ConflitoHorarioError):
            self.agenda.marcar("Bruno", "Dr. Silva", "2026-10-05", 9, 30)

    def test_profissionais_diferentes_nao_conflitam(self):
        self.agenda.marcar("Ana", "Dr. Silva", "2026-10-05", 9, 30)
        self.agenda.marcar("Bruno", "Dra. Souza", "2026-10-05", 9, 30)
        self.assertEqual(len(self.agenda.listar_por_data("2026-10-05")), 2)

    def test_conflito_nao_altera_a_agenda(self):
        self.agenda.marcar("Ana", "Dr. Silva", "2026-10-05", 9, 30)
        with self.assertRaises(ConflitoHorarioError):
            self.agenda.marcar("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
        self.assertEqual(len(self.agenda.listar_por_data("2026-10-05")), 1)

    def test_entradas_invalidas_nao_alteram_a_agenda(self):
        casos = [
            ("Ana", "Dr. Silva", "2026-10-05", 20, 30),  # o caso das 20h
            ("Ana", "Dr. Silva", "2026-10-05", 7, 30),
            ("Ana", "Dr. Silva", "2026-10-05", 17, 75),  # termina apos 18h
            ("Ana", "Dr. Silva", "2026-10-05", 9, 10),
            ("Ana", "Dr. Silva", "2026-10-05", 9, 135),
            ("Ana", "Dr. Silva", "05/10/2026", 9, 30),
            ("", "Dr. Silva", "2026-10-05", 9, 30),
            ("Ana", None, "2026-10-05", 9, 30),
        ]
        for caso in casos:
            with self.subTest(caso=caso):
                with self.assertRaises(EntradaInvalidaError):
                    self.agenda.marcar(*caso)
        self.assertEqual(self.agenda.listar_por_data("2026-10-05"), [])


class RemarcarTest(unittest.TestCase):
    def setUp(self):
        self.agenda = Agenda()
        self.agenda.marcar("Ana", "Dr. Silva", "2026-10-05", 9, 30)
        self.agenda.marcar("Bruno", "Dr. Silva", "2026-10-05", 10, 30)

    def test_remarca_para_horario_livre(self):
        r = self.agenda.remarcar("Ana", "2026-10-05", 9, "2026-10-06", 10)
        self.assertEqual((r.data.isoformat(), r.hora_inicio), ("2026-10-06", 10))
        self.assertEqual(len(self.agenda.listar_por_data("2026-10-05")), 1)
        self.assertEqual(len(self.agenda.listar_por_data("2026-10-06")), 1)

    def test_conflito_no_novo_horario(self):
        with self.assertRaises(ConflitoHorarioError):
            self.agenda.remarcar("Ana", "2026-10-05", 9, "2026-10-05", 10)

    def test_atendimento_inexistente(self):
        with self.assertRaises(AtendimentoNaoEncontradoError):
            self.agenda.remarcar("Zed", "2026-10-05", 9, "2026-10-06", 10)

    def test_novo_horario_fora_do_expediente(self):
        with self.assertRaises(EntradaInvalidaError):
            self.agenda.remarcar("Ana", "2026-10-05", 9, "2026-10-06", 20)

    def test_nova_hora_que_estoura_o_fechamento(self):
        agenda = Agenda()
        agenda.marcar("Ana", "Dr. Silva", "2026-10-05", 9, 120)
        with self.assertRaises(EntradaInvalidaError):
            agenda.remarcar("Ana", "2026-10-05", 9, "2026-10-06", 17)

    def test_remarcacao_mantem_a_ordem_de_listagem(self):
        self.agenda.remarcar("Ana", "2026-10-05", 9, "2026-10-05", 11)
        horas = [a.hora_inicio for a in self.agenda.listar_por_data("2026-10-05")]
        self.assertEqual(horas, [11, 10])

    def test_remarcar_para_o_mesmo_horario_e_conflito(self):
        # Comportamento do codigo original, mantido de proposito.
        with self.assertRaises(ConflitoHorarioError):
            self.agenda.remarcar("Ana", "2026-10-05", 9, "2026-10-05", 9)

    def test_entrada_invalida(self):
        with self.assertRaises(EntradaInvalidaError):
            self.agenda.remarcar("Ana", "ontem", 9, "2026-10-06", 10)


class ListarTest(unittest.TestCase):
    def test_dia_sem_atendimentos(self):
        self.assertEqual(Agenda().listar_por_data("2026-10-05"), [])

    def test_data_invalida(self):
        with self.assertRaises(EntradaInvalidaError):
            Agenda().listar_por_data("hoje")


if __name__ == "__main__":
    unittest.main()