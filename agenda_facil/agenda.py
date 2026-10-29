"""Regras de agendamento: marcar, remarcar e consultar atendimentos."""

from dataclasses import replace

from .excecoes import AtendimentoNaoEncontradoError, ConflitoHorarioError
from .validacao import (
    criar_atendimento,
    validar_data,
    validar_hora_inicio,
    validar_termino_no_expediente,
    validar_texto_obrigatorio,
)


class Agenda:
    """Agenda de atendimentos de uma clínica, mantida em memória.

    Esta classe não imprime nada: informa o resultado por retorno ou exceção
    e deixa a apresentação para :mod:`agenda_facil.apresentacao`.
    """

    def __init__(self):
        """Cria uma agenda vazia."""
        self._atendimentos = []

    def marcar(self, paciente, profissional, data, hora_inicio, duracao_minutos):
        """Marca um novo atendimento.

        Args:
            paciente: Nome do paciente (texto não vazio).
            profissional: Nome do profissional (texto não vazio).
            data: Data no formato `AAAA-MM-DD`.
            hora_inicio: Hora cheia de início (8 a 17).
            duracao_minutos: Duração em minutos (15 a 120, múltiplo de 15);
                o atendimento deve terminar até as 18h.

        Returns:
            Atendimento: O atendimento recém-marcado.

        Raises:
            EntradaInvalidaError: Se alguma entrada violar as regras de negócio.
            ConflitoHorarioError: Se o profissional já tiver atendimento no
                mesmo dia e horário.
        """
        atendimento = criar_atendimento(
            paciente, profissional, data, hora_inicio, duracao_minutos
        )
        self._garantir_horario_livre(
            atendimento.profissional, atendimento.data, atendimento.hora_inicio
        )
        self._atendimentos.append(atendimento)
        return atendimento

    def remarcar(self, paciente, data, hora_inicio, nova_data, nova_hora_inicio):
        """Muda o dia e a hora de um atendimento já marcado.

        O atendimento é localizado por paciente, data e hora. Se houver mais de
        um com essa mesma chave, o primeiro marcado é o remarcado.

        Args:
            paciente: Nome do paciente do atendimento a remarcar.
            data: Data atual do atendimento, no formato `AAAA-MM-DD`.
            hora_inicio: Hora de início atual do atendimento.
            nova_data: Nova data, no formato `AAAA-MM-DD`.
            nova_hora_inicio: Nova hora cheia de início (8 a 17).

        Returns:
            Atendimento: O atendimento já com a nova data e hora.

        Raises:
            EntradaInvalidaError: Se alguma entrada for inválida, ou se a nova
                hora, somada à duração do atendimento, passar das 18h.
            AtendimentoNaoEncontradoError: Se não existir o atendimento informado.
            ConflitoHorarioError: Se o profissional já estiver ocupado no novo
                dia e horário.
        """
        paciente = validar_texto_obrigatorio(paciente, "paciente")
        data_atual = validar_data(data)
        hora_atual = validar_hora_inicio(hora_inicio)
        data_nova = validar_data(nova_data)
        hora_nova = validar_hora_inicio(nova_hora_inicio)

        posicao = self._posicao_do_atendimento(paciente, data_atual, hora_atual)
        atendimento = self._atendimentos[posicao]
        validar_termino_no_expediente(hora_nova, atendimento.duracao_minutos)
        self._garantir_horario_livre(atendimento.profissional, data_nova, hora_nova)

        remarcado = replace(atendimento, data=data_nova, hora_inicio=hora_nova)
        # Substitui na mesma posição para não alterar a ordem de listagem.
        self._atendimentos[posicao] = remarcado
        return remarcado

    def listar_por_data(self, data):
        """Lista os atendimentos de um dia, na ordem em que foram marcados.

        Args:
            data: Data no formato `AAAA-MM-DD`.

        Returns:
            list[Atendimento]: Atendimentos do dia (lista vazia se não houver).

        Raises:
            EntradaInvalidaError: Se `data` não estiver no formato `AAAA-MM-DD`.
        """
        data_consultada = validar_data(data)
        return [a for a in self._atendimentos if a.data == data_consultada]

    def _existe_conflito(self, profissional, data, hora_inicio):
        """Diz se o profissional já tem atendimento nesse dia e hora.

        Único lugar onde a regra de conflito existe. Usa `any` para parar no
        primeiro conflito, em vez de varrer a lista inteira.
        """
        return any(
            a.profissional == profissional
            and a.data == data
            and a.hora_inicio == hora_inicio
            for a in self._atendimentos
        )

    def _garantir_horario_livre(self, profissional, data, hora_inicio):
        """Levanta :class:`ConflitoHorarioError` se o horário já estiver ocupado."""
        # Na remarcação o próprio atendimento ainda está na lista, então
        # remarcar para o mesmo horário conta como conflito. É o comportamento
        # do código original e foi mantido de propósito.
        if self._existe_conflito(profissional, data, hora_inicio):
            raise ConflitoHorarioError(
                f"{profissional} ja possui atendimento em {data.isoformat()} "
                f"as {hora_inicio}h"
            )

    def _posicao_do_atendimento(self, paciente, data, hora_inicio):
        """Devolve o índice do atendimento do paciente nesse dia e hora."""
        for posicao, atendimento in enumerate(self._atendimentos):
            if (
                atendimento.paciente == paciente
                and atendimento.data == data
                and atendimento.hora_inicio == hora_inicio
            ):
                return posicao
        raise AtendimentoNaoEncontradoError(
            f"nenhum atendimento de {paciente!r} em {data.isoformat()} as {hora_inicio}h"
        )