"""Formatação e exibição de mensagens. É a única camada que usa `print`."""

from .constantes import (
    MENSAGEM_HORARIO_OCUPADO,
    MENSAGEM_REMARCADO,
    PREFIXO_MENSAGEM_MARCADO,
)


def formatar_marcacao(atendimento):
    """Monta a mensagem de confirmação de um atendimento marcado.

    Args:
        atendimento: Atendimento recém-marcado.

    Returns:
        str: Ex.: `"Atendimento marcado para Ana"`.
    """
    return f"{PREFIXO_MENSAGEM_MARCADO} {atendimento.paciente}"


def formatar_linha_atendimento(atendimento):
    """Monta a linha de listagem de um atendimento.

    Args:
        atendimento: Atendimento a exibir.

    Returns:
        str: Hora, paciente, profissional e status separados por espaço.
    """
    return (
        f"{atendimento.hora_inicio} {atendimento.paciente} "
        f"{atendimento.profissional} {atendimento.status}"
    )


def exibir_marcacao(atendimento):
    """Imprime a confirmação de um atendimento marcado."""
    print(formatar_marcacao(atendimento))


def exibir_remarcacao():
    """Imprime a confirmação de uma remarcação."""
    print(MENSAGEM_REMARCADO)


def exibir_horario_ocupado():
    """Imprime o aviso de que o horário está ocupado."""
    print(MENSAGEM_HORARIO_OCUPADO)


def exibir_atendimentos(atendimentos):
    """Imprime uma linha para cada atendimento da sequência.

    Args:
        atendimentos: Sequência de :class:Atendimento.
    """
    for atendimento in atendimentos:
        print(formatar_linha_atendimento(atendimento))