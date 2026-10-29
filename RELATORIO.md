# Relatório — AgendaFácil

## 1. Diagnóstico do código-base (Etapa 1)

Linhas referentes ao arquivo original `agenda_base.py`.

| # | Categoria | Anomalia encontrada (e onde) | Por que é um problema |
|---|-----------|------------------------------|-----------------------|
| 1 | Adequação e lógica | `add` só valida `h >= 8`, `h < 18` e `dur > 0` (l. 14–16). Não exige duração de 15 a 120 nem múltipla de 15, e não confere se o atendimento termina às 18h (ex.: 17h com 120 min passa). | O sistema aceita atendimentos que violam as regras de negócio e ficam gravados na agenda. |
| 2 | Adequação e lógica | `rem` não valida a nova data nem a nova hora (l. 30–43): dá para remarcar para as 20h ou para uma data qualquer. | Contorna o expediente: a regra vale ao marcar, mas não ao remarcar. |
| 3 | Adequação e lógica | O `for` de `rem` não tem `break` (l. 32–43): se houver dois atendimentos com a mesma chave, ambos são alterados e "Remarcado" é impresso duas vezes. | Remarca atendimentos que ninguém pediu para remarcar. |
| 4 | Adequação e lógica | O comentário de `lst` diz "do mês" (l. 53), mas a função filtra por dia (`a[2] == d`). | Comentário contradiz o código e induz a erro. |
| 5 | Manutenibilidade | Números e textos de negócio soltos: `8`, `18` e `"MARCADO"` (l. 14, 15, 22); mensagens repetidas no código (l. 23, 25, 41, 43). | Mudar o expediente ou uma mensagem exige caçar valores espalhados, com risco de esquecer um. |
| 6 | Manutenibilidade | O atendimento é uma lista acessada por posição: `a[0]`…`a[5]` (l. 19, 33, 36, 56). | Ninguém sabe o que é `a[3]` sem ler o `append`; trocar a ordem dos campos quebra tudo em silêncio. |
| 7 | Manutenibilidade | A regra de conflito aparece duas vezes, copiada em `add` (l. 18–20) e em `rem` (l. 35–37). | Corrigir a regra em um lugar e esquecer o outro gera inconsistência. |
| 8 | Manutenibilidade | Estado global mutável `ag` (l. 8) usado por todas as funções. | Impossível testar de forma isolada ou ter duas agendas; testes interferem entre si. |
| 9 | Organização e estética | Nomes crípticos: `ag`, `p`, `pr`, `d`, `h`, `dur`, `nd`, `nh`, `ok`, `add`, `rem`, `lst`. Fora do PEP 8 e sem significado. | O leitor precisa deduzir o que cada nome representa. |
| 10 | Organização e estética | `add` mistura validação, conflito, inserção e `print`; `rem` mistura busca, conflito, alteração e `print` (l. 11–43). Aninhamento de 5 níveis de `if` em `add`. | Funções com várias responsabilidades são difíceis de ler, testar e reutilizar. |
| 11 | Organização e estética | Ruído: cabeçalho com histórico de alterações (l. 1–6), código morto comentado (l. 46–47), TODO vencido (l. 49), comentários que repetem o código (l. 12, 31). | Informação que o controle de versão já guarda, ou que não diz nada, polui a leitura. |
| 12 | Organização e estética | O código de demonstração roda no nível do módulo (l. 59–63), sem `if __name__ == "__main__"`, e tudo vive em um único arquivo. | Importar o arquivo já executa o programa e imprime coisas; nada pode ser reutilizado. |
| 13 | Programação defensiva | `except: pass` (l. 26–27) engole qualquer erro, inclusive `TypeError` (ex.: `h="9"`) e `KeyboardInterrupt`. | Falhas desaparecem sem rastro e ninguém descobre o que aconteceu. |
| 14 | Programação defensiva | Entrada inválida não gera erro nem mensagem: `add("Ana", ..., 20, 30)` não faz nada (l. 14–16 sem `else`). | O usuário acha que marcou e o atendimento nunca existiu. |
| 15 | Programação defensiva | Nenhuma checagem de tipo ou formato: `d` é qualquer valor (l. 19, 33); `"05/10/2026"`, `None` e `"hoje"` são aceitos como data; nome do paciente pode ser vazio. | Dados sujos entram na agenda e quebram a listagem e a comparação depois. |
| 16 | Programação defensiva | `rem` de um atendimento inexistente não faz nada nem avisa (l. 32–43). | Falha silenciosa: quem chamou não sabe que a remarcação não ocorreu. |
| 17 | Desempenho e recursos | O laço de conflito em `add` percorre a lista inteira mesmo depois de achar o conflito (l. 18–20, sem `break`). | Trabalho desnecessário em toda marcação. |
| 18 | Desempenho e recursos | `rem` tem laço dentro de laço (l. 32–37): custo O(n²). | Cresce rápido com o volume de atendimentos. |
| 19 | Desempenho e recursos | `lst` varre todos os atendimentos de todos os dias para listar um dia (l. 54–56). | Custo proporcional à agenda inteira para uma consulta de um dia só. |

Esta tabela é a linha de base da refatoração; a seção 2 diz o que foi resolvido
e o que ficou como dívida técnica.

## 2. O que foi resolvido e dívida técnica assumida

### Resolvido

| Anomalia | Como foi resolvida |
|----------|--------------------|
| 5 | Valores e mensagens em `constantes.py`. |
| 6 | `Atendimento` virou uma `dataclass(frozen=True)` com campos nomeados. |
| 7 | Regra de conflito em um único método, `Agenda._existe_conflito`, usado por marcar e remarcar. |
| 8 | Estado encapsulado na classe `Agenda`; sem variável global. |
| 9, 4 | Nomes descritivos em PEP 8 (snake_case, PascalCase, MAIUSCULAS); comentários corrigidos. |
| 10 | Validação (`validacao.py`), regras (`agenda.py`) e saída (`apresentacao.py`) separadas; `Agenda` não imprime. |
| 11, 12 | Cabeçalho, código morto e TODO removidos; demonstração em `demonstracao.py`, chamada por `main.py` e `__main__.py`. |
| 1, 2, 15 | Duração, término no expediente, data e textos validados ao marcar **e** ao remarcar. |
| 3 | Remarcação localiza um único atendimento (o primeiro com a chave) e o substitui. |
| 13, 14, 16 | Sem `except` vazio; entradas inválidas levantam `EntradaInvalidaError`; atendimento inexistente levanta `AtendimentoNaoEncontradoError`. |
| 17 | Verificação de conflito com `any`, que para no primeiro conflito. |

### Dívida técnica assumida (decidi deixar)

* **Desempenho (18, 19):** a agenda continua sendo uma lista percorrida
  linearmente. Para uma clínica pequena, em memória, isso é suficiente; indexar
  por (profissional, data, hora) só adicionaria complexidade sem ganho
  perceptível. Se o volume crescer, o lugar de trocar é `Agenda`, sem afetar o
  resto.
* **Conflito só por horário de início:** a regra pedida é "mesmo dia e horário"
  e o código-base compara apenas a hora de início. Um atendimento de 9h com 120
  min e outro às 10h do mesmo profissional **não** são considerados conflito.
  Tratar sobreposição de intervalos seria mudança de regra de negócio.
* **Remarcar para o mesmo horário** continua sendo conflito (o próprio
  atendimento ainda está na lista), como no código-base. Está coberto por teste.
* **Sem `desmarcar`:** estava só comentado no original e não faz parte do
  escopo.
* **Sem persistência:** os dados vivem em memória, por restrição do enunciado.

## 3. Comportamento: o que permanece e o que muda

**Caminho feliz idêntico.** `python3 main.py` imprime exatamente a mesma saída
do `agenda_base.py` (conferido com `diff` e por teste automatizado).

**Mudanças de propósito para entradas inválidas** (Etapa 4):

| Entrada | Antes | Agora |
|---------|-------|-------|
| Marcar às 20h (ou antes das 8h) | Nada acontecia, sem aviso | `EntradaInvalidaError` |
| Duração fora de 15–120 ou não múltipla de 15 | Aceita se `> 0` | `EntradaInvalidaError` |
| Atendimento que termina depois das 18h | Aceito | `EntradaInvalidaError` |
| Data fora do formato `AAAA-MM-DD` (ou inexistente, como 30/02) | Aceita | `EntradaInvalidaError` |
| Paciente/profissional vazio ou não texto | Aceito | `EntradaInvalidaError` |
| Remarcar para hora fora do expediente | Aceito | `EntradaInvalidaError` |
| Remarcar atendimento inexistente | Nada acontecia | `AtendimentoNaoEncontradoError` |
| Qualquer erro dentro de `add` | Engolido por `except: pass` | Propaga |

## 4. Decisão de projeto relevante

O conflito de horário é tratado de forma diferente da entrada inválida de
propósito: conflito é um desfecho esperado no dia a dia da clínica, então a
demonstração o captura e mostra "Horario ocupado", como o código-base fazia.
Entrada inválida é erro de quem chamou, então propaga como exceção específica,
com mensagem que diz o que está errado e qual valor causou o problema.
`EntradaInvalidaError` herda também de `ValueError`, para que quem já captura
`ValueError` continue funcionando. O `Atendimento` é imutável: remarcar gera um
novo objeto na mesma posição da lista, o que preserva a ordem de listagem
(necessária para manter a saída original) e evita alterações acidentais.

## 5. Como executar e testar

```bash
python3 main.py              # demonstração
python3 -m unittest -v       # 31 testes automatizados
pip install pdoc && python3 -m pdoc --docformat google agenda_facil -o docs
```

## 6. Divisão do trabalho

| # | Quem | Commit |
|---|------|--------|
| 1 | Júlio César | docs: diagnóstico do código-base (Etapa 1) |
| 2 | Júlio César | refactor: constantes, exceções, modelo e validação de entradas |
| 3 | Gustavo Matheus | refactor: Agenda, apresentação e demonstração; remove agenda_base.py |
| 4 | Gustavo Matheus | docs: README, testes e documentação de API (pdoc) |
| 5 | Júlio César | docs: relatório completo (decisões, mudanças e execução) |