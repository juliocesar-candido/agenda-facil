"""AgendaFácil: agenda de atendimentos de uma clínica pequena.

Uso básico::

    from agenda_facil import Agenda

    agenda = Agenda()
    agenda.marcar("Ana", "Dr. Silva", "2026-10-05", 9, 30)
"""

from .agenda import Agenda
from .excecoes import (
    AgendaFacilError,
    AtendimentoNaoEncontradoError,
    ConflitoHorarioError,
    EntradaInvalidaError,
)
from .modelos import Atendimento

__all__ = [
    "Agenda",
    "Atendimento",
    "AgendaFacilError",
    "AtendimentoNaoEncontradoError",
    "ConflitoHorarioError",
    "EntradaInvalidaError",
]