"""Programa de demonstração do AgendaFácil (mesmo roteiro do código-base)."""

from . import apresentacao
from .agenda import Agenda
from .excecoes import ConflitoHorarioError


def marcar_e_informar(agenda, paciente, profissional, data, hora_inicio, duracao_minutos):
    """Marca um atendimento e imprime o resultado.

    Conflito de horário é um desfecho esperado no dia a dia da clínica, por
    isso vira aviso na tela. Entradas inválidas NÃO são capturadas aqui:
    propagam para quem chamou.

    Args:
        agenda: Agenda onde marcar.
        paciente: Nome do paciente.
        profissional: Nome do profissional.
        data: Data no formato `AAAA-MM-DD`.
        hora_inicio: Hora cheia de início.
        duracao_minutos: Duração em minutos.

    Raises:
        EntradaInvalidaError: Se alguma entrada for inválida.
    """
    try:
        atendimento = agenda.marcar(paciente, profissional, data, hora_inicio, duracao_minutos)
    except ConflitoHorarioError:
        apresentacao.exibir_horario_ocupado()
    else:
        apresentacao.exibir_marcacao(atendimento)


def remarcar_e_informar(agenda, paciente, data, hora_inicio, nova_data, nova_hora_inicio):
    """Remarca um atendimento e imprime o resultado.

    Args:
        agenda: Agenda onde remarcar.
        paciente: Nome do paciente.
        data: Data atual, no formato `AAAA-MM-DD`.
        hora_inicio: Hora de início atual.
        nova_data: Nova data, no formato `AAAA-MM-DD`.
        nova_hora_inicio: Nova hora de início.

    Raises:
        EntradaInvalidaError: Se alguma entrada for inválida.
        AtendimentoNaoEncontradoError: Se o atendimento não existir.
    """
    try:
        agenda.remarcar(paciente, data, hora_inicio, nova_data, nova_hora_inicio)
    except ConflitoHorarioError:
        apresentacao.exibir_horario_ocupado()
    else:
        apresentacao.exibir_remarcacao()


def executar_demonstracao():
    """Executa o roteiro de demonstração do código-base original."""
    agenda = Agenda()
    marcar_e_informar(agenda, "Ana", "Dr. Silva", "2026-10-05", 9, 30)
    marcar_e_informar(agenda, "Bruno", "Dr. Silva", "2026-10-05", 9, 30)
    marcar_e_informar(agenda, "Carla", "Dra. Souza", "2026-10-05", 14, 60)
    remarcar_e_informar(agenda, "Ana", "2026-10-05", 9, "2026-10-06", 10)
    apresentacao.exibir_atendimentos(agenda.listar_por_data("2026-10-05"))