"""Exceções específicas do AgendaFácil."""


class AgendaFacilError(Exception):
    """Base de todos os erros levantados pelo AgendaFácil."""


class EntradaInvalidaError(AgendaFacilError, ValueError):
    """Um argumento recebido viola uma pré-condição (formato, tipo ou faixa).

    Herda também de ``ValueError`` para que quem já captura ``ValueError``
    continue funcionando.
    """


class ConflitoHorarioError(AgendaFacilError):
    """O profissional já possui atendimento no mesmo dia e horário."""


class AtendimentoNaoEncontradoError(AgendaFacilError):
    """Nenhum atendimento corresponde ao paciente, data e hora informados."""