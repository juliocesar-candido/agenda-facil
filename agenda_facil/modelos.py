"""Modelos e estruturas de dados do domínio."""

from dataclasses import dataclass
from datetime import date

from .constantes import STATUS_MARCADO


@dataclass(frozen=True)
class Atendimento:
    """Representa um agendamento na clínica

    como esta classe é imutável, qualquer remarcação gera uma nova instância de
    atendimento em vez de alterar a existente, para garantir a consistência, crie
    novas instâncias apenas via :func:`agenda_facil.validacao.criar_atendimento`

    Attributes:
        paciente: nome do paciente agendado
        profissional: profissional responsável pelo atendimento
        data: data da consulta
        hora_inicio: horário de início em formato de hora cheia (8 a 17)
        duracao_minutos: duração total da consulta em minutos
        status: estado atual do agendamento, padrão: marcado
    """

    paciente: str
    profissional: str
    data: date
    hora_inicio: int
    duracao_minutos: int
    status: str = STATUS_MARCADO