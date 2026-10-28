"""Valida e limpa as entradas antes de criar um agendamento.

Garante que só dados corretos entrem no sistema, evitando
ter que repetir checagens no resto do código.
"""

import re
from datetime import date

from .constantes import (
    DURACAO_MAXIMA_MINUTOS,
    DURACAO_MINIMA_MINUTOS,
    FORMATO_DATA,
    HORA_ABERTURA,
    HORA_FECHAMENTO,
    MINUTOS_POR_HORA,
    PASSO_DURACAO_MINUTOS,
    ULTIMA_HORA_INICIO,
)
from .excecoes import EntradaInvalidaError
from .modelos import Atendimento

# Só dígitos ASCII para que não seja aceito também dígitos de outros alfabetos
_PADRAO_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


def validar_texto_obrigatorio(valor, nome_campo):
    """Garante que ``valor`` é um texto não vazio e o devolve sem espaços nas pontas

    Args:
        valor: valor recebido do chamador
        nome_campo: Nome do campo, usado na mensagem de erro

    Returns:
        str: o texto sem espaços no início e no fim

    Raises:
        EntradaInvalidaError: se ``valor`` não for ``str`` ou estiver vazio
    """
    if not isinstance(valor, str):
        raise EntradaInvalidaError(
            f"{nome_campo} deve ser texto, mas recebeu {valor!r} ({type(valor).__name__})"
        )
    texto = valor.strip()
    if not texto:
        raise EntradaInvalidaError(f"{nome_campo} nao pode ser vazio: recebeu {valor!r}")
    return texto


def validar_data(valor):
    """Converte um texto ``AAAA-MM-DD`` em ``date``.

    Args:
        valor: data no formato ``AAAA-MM-DD``.

    Returns:
        datetime.date: a data correspondente.

    Raises:
        EntradaInvalidaError: se não for texto, se o formato for outro ou se a
            data não existir no calendário (ex.: ``2026-02-30``).
    """
    if not isinstance(valor, str) or not _PADRAO_DATA.fullmatch(valor):
        raise EntradaInvalidaError(
            f"data invalida: {valor!r} (formato esperado: {FORMATO_DATA})"
        )
    try:
        return date.fromisoformat(valor)
    except ValueError:
        raise EntradaInvalidaError(
            f"data invalida: {valor!r} (nao existe no calendario)"
        ) from None


def _eh_inteiro(valor):
    # bool é subclasse de int em Python, mas True/False não são horas nem durações.
    return isinstance(valor, int) and not isinstance(valor, bool)


def validar_hora_inicio(valor):
    """Garante que a hora de início está dentro do expediente.

    A hora é um inteiro (hora cheia), pois o sistema original só trabalha com
    horas cheias; minutos de início não existem neste modelo.

    Args:
        valor: Hora de início, de ``HORA_ABERTURA`` a ``ULTIMA_HORA_INICIO``.

    Returns:
        int: a própria hora, já validada

    Raises:
        EntradaInvalidaError: se não for inteiro ou estiver fora do expediente
    """
    if not _eh_inteiro(valor) or not HORA_ABERTURA <= valor <= ULTIMA_HORA_INICIO:
        raise EntradaInvalidaError(
            f"hora de inicio invalida: {valor!r} "
            f"(esperado inteiro entre {HORA_ABERTURA} e {ULTIMA_HORA_INICIO})"
        )
    return valor


def validar_duracao(valor):
    """Garante que a duração está na faixa permitida e em múltiplos do passo

    Args:
        valor: duração em minutos

    Returns:
        int: a própria duração, já validada

    Raises:
        EntradaInvalidaError: se não for inteiro, estiver fora da faixa ou não
            for múltiplo de ``PASSO_DURACAO_MINUTOS``
    """
    if (
        not _eh_inteiro(valor)
        or not DURACAO_MINIMA_MINUTOS <= valor <= DURACAO_MAXIMA_MINUTOS
        or valor % PASSO_DURACAO_MINUTOS != 0
    ):
        raise EntradaInvalidaError(
            f"duracao invalida: {valor!r} (esperado multiplo de "
            f"{PASSO_DURACAO_MINUTOS} entre {DURACAO_MINIMA_MINUTOS} e "
            f"{DURACAO_MAXIMA_MINUTOS} minutos)"
        )
    return valor


def validar_termino_no_expediente(hora_inicio, duracao_minutos):
    """Garante que o atendimento termina até o fechamento da clínica

    Args:
        hora_inicio: hora de início já validada.
        duracao_minutos: duração em minutos já validada

    Raises:
        EntradaInvalidaError: se o término passar de ``HORA_FECHAMENTO``
    """
    termino_em_minutos = hora_inicio * MINUTOS_POR_HORA + duracao_minutos
    if termino_em_minutos > HORA_FECHAMENTO * MINUTOS_POR_HORA:
        raise EntradaInvalidaError(
            f"atendimento comecando as {hora_inicio}h com {duracao_minutos} min "
            f"termina depois do fechamento ({HORA_FECHAMENTO}h)"
        )


def criar_atendimento(paciente, profissional, data, hora_inicio, duracao_minutos):
    """Valida todas as entradas e constrói o :class:`Atendimento` correspondente

    Args:
        paciente: nome do paciente (texto não vazio)
        profissional: nome do profissional (texto não vazio)
        data: Data no formato ``AAAA-MM-DD``
        hora_inicio: hora cheia de início, dentro do expediente
        duracao_minutos: duração em minutos (15 a 120, múltiplo de 15)

    Returns:
        Atendimento: atendimento com todos os campos validados

    Raises:
        EntradaInvalidaError: se qualquer entrada violar as regras de negócio
    """
    paciente = validar_texto_obrigatorio(paciente, "paciente")
    profissional = validar_texto_obrigatorio(profissional, "profissional")
    data_validada = validar_data(data)
    hora_validada = validar_hora_inicio(hora_inicio)
    duracao_validada = validar_duracao(duracao_minutos)
    validar_termino_no_expediente(hora_validada, duracao_validada)
    return Atendimento(
        paciente=paciente,
        profissional=profissional,
        data=data_validada,
        hora_inicio=hora_validada,
        duracao_minutos=duracao_validada,
    )