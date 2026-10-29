# AgendaFácil

Agenda de atendimentos de uma clínica pequena: **marca** um atendimento,
**remarca** e **lista** o que está agendado em um dia. Os dados vivem em
memória (sem banco de dados e sem interface gráfica).

Este repositório é a refatoração do código-base `agenda_base.py` (organização,
documentação e programação defensiva), sem funcionalidade nova. As decisões e o
diagnóstico estão em [`RELATORIO.md`](RELATORIO.md).

## Requisitos

- Python **3.10 ou superior**
- Nenhuma dependência externa para rodar o programa e os testes.
- Apenas para gerar a documentação: [`pdoc`](https://pdoc.dev) (ferramenta de
  desenvolvimento, não faz parte do programa).

## Estrutura

```
agenda_facil/
  __init__.py      # API pública do pacote
  __main__.py      # python3 -m agenda_facil
  agenda.py        # regras de agendamento (classe Agenda)
  apresentacao.py  # única camada que usa print
  constantes.py    # valores fixos com significado de negócio
  demonstracao.py  # programa de demonstração do código-base
  excecoes.py      # exceções específicas
  modelos.py       # dataclass Atendimento
  validacao.py     # validação das entradas
tests/             # testes automatizados (unittest)
docs/              # documentação de API gerada com pdoc
main.py            # ponto de entrada
```

## Como compilar

Python é interpretado, então não há etapa de compilação. Para apenas conferir
que todos os arquivos são sintaticamente válidos:

```bash
python3 -m compileall agenda_facil main.py
```

> No Windows, use `python` (ou `py`) no lugar de `python3`.

## Como executar

Na raiz do repositório, qualquer um dos dois comandos roda a demonstração:

```bash
python3 main.py
python3 -m agenda_facil
```

Saída esperada (idêntica à do código-base):

```
Atendimento marcado para Ana
Horario ocupado
Atendimento marcado para Carla
Remarcado
14 Carla Dra. Souza MARCADO
```

### Usando como biblioteca

```python
from agenda_facil import Agenda, ConflitoHorarioError, EntradaInvalidaError

agenda = Agenda()
agenda.marcar("Ana", "Dr. Silva", "2026-10-05", 9, 30)

try:
    agenda.marcar("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
except ConflitoHorarioError as erro:
    print(erro)

agenda.remarcar("Ana", "2026-10-05", 9, "2026-10-06", 10)
print(agenda.listar_por_data("2026-10-06"))
```

## Regras de negócio

| Regra     | Definição                                                                  |
|-----------|----------------------------------------------------------------------------|
| Expediente| Começa entre 8h e 17h; o atendimento termina até as 18h.                   |
| Duração   | De 15 a 120 minutos, em múltiplos de 15.                                   |
| Conflito  | Um profissional não pode ter dois atendimentos no mesmo dia e horário.     |
| Data      | Formato `AAAA-MM-DD`. Qualquer outro formato é entrada inválida.           |

Entradas inválidas levantam `EntradaInvalidaError` (que também é um
`ValueError`); conflito levanta `ConflitoHorarioError`; remarcar algo que não
existe levanta `AtendimentoNaoEncontradoError`. Todas herdam de
`AgendaFacilError`.

## Como rodar os testes

```bash
python3 -m unittest -v
```

## Como gerar a documentação de API

```bash
pip install pdoc
python3 -m pdoc --docformat google agenda_facil -o docs
```

Depois abra `docs/index.html` no navegador. A pasta `docs/` já vem versionada
no repositório; o comando acima só é necessário para regenerá-la.

## Grupo

- Gustavo Matheus Tomé de Sousa
- Júlio César Cândido de Santana