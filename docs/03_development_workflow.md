# WINQuantLab

> Biblioteca Python para pesquisa quantitativa aplicada ao mercado financeiro.

---

# Documento

Development Workflow

Versão: 1.0

Status: Em desenvolvimento

Última atualização: 2026-08-07

---

# 1. Objetivo

Este documento define o processo oficial de desenvolvimento do WINQuantLab.

Todas as novas funcionalidades deverão seguir este fluxo para garantir consistência, qualidade, reutilização de código e facilidade de manutenção.

---

# 2. Filosofia de Desenvolvimento

O desenvolvimento do WINQuantLab é baseado em cinco pilares.

- Arquitetura antes da implementação.
- Desenvolvimento orientado por testes (TDD).
- Reutilização de componentes.
- Código simples e legível.
- Evolução incremental.

Antes de escrever qualquer código, deve existir uma compreensão clara do problema e de sua solução.

---

# 3. Fluxo de Desenvolvimento

Toda nova funcionalidade seguirá obrigatoriamente o fluxo abaixo.

```text
Necessidade

↓

Estudo da matemática

↓

Identificação de reutilização

↓

Implementação da base matemática

↓

Testes da base matemática

↓

Implementação da funcionalidade

↓

Testes da funcionalidade

↓

Refatoração (quando necessária)

↓

Documentação

↓

Git Commit
```

Nenhuma etapa deve ser ignorada.

---

# 4. Desenvolvimento de Indicadores

A implementação de um novo indicador seguirá sempre a sequência abaixo.

## Etapa 1

Estudar a fórmula matemática.

Responder perguntas como:

- Quais dados são utilizados?
- Existe suavização?
- Existe janela móvel?
- Existe cálculo acumulado?
- Existe dependência de outro indicador?

---

## Etapa 2

Identificar reutilização.

Antes de criar qualquer função, verificar se o cálculo já existe.

Caso não exista:

- implementar no menor escopo possível.

---

## Etapa 3

Implementar cálculos reutilizáveis.

Quando um cálculo puder ser reutilizado por outros indicadores, ele deverá ser separado da implementação principal.

---

## Etapa 4

Criar testes da matemática.

A matemática deve ser validada antes da implementação do indicador.

---

## Etapa 5

Implementar o indicador.

O indicador deverá reutilizar os cálculos existentes sempre que possível.

---

## Etapa 6

Criar testes do indicador.

Devem existir testes para:

- criação das colunas;
- validação de parâmetros;
- ausência de colunas obrigatórias;
- preservação do DataFrame original;
- validação matemática;
- casos extremos.

---

## Etapa 7

Atualizar documentação.

Atualizar os documentos afetados pela nova funcionalidade.

---

# 5. Reutilização de Código

Toda nova função deverá nascer no menor escopo possível.

Hierarquia oficial:

```text
Indicador

↓

Família

↓

Projeto
```

Regras:

- Funções utilizadas apenas por um indicador permanecem nele.
- Funções reutilizadas por uma família vão para `family/calculations.py`.
- Funções reutilizadas entre famílias vão para `indicators/calculations.py`.

Essa abordagem evita abstrações prematuras.

---

# 6. Refatoração

Refatorações não deverão interromper uma sprint ou epic em andamento.

Uma refatoração somente deverá ocorrer quando existir pelo menos um dos seguintes motivos:

- correção de bug;
- necessidade funcional;
- reutilização por múltiplos módulos;
- melhoria arquitetural significativa.

Mudanças apenas estéticas deverão ser evitadas durante o desenvolvimento de uma funcionalidade.

---

# 7. Desenvolvimento Orientado por Testes

O WINQuantLab utiliza TDD como metodologia oficial.

Fluxo:

```text
RED

↓

GREEN

↓

REFACTOR
```

Primeiro escreve-se o teste.

Depois implementa-se o código.

Por último realiza-se a refatoração necessária.

---

# 8. Atualização da Documentação

Sempre que uma funcionalidade for concluída deverão ser avaliados os seguintes documentos.

- CHANGELOG
- README
- Product Vision (quando necessário)
- Architecture (quando necessário)
- Roadmap
- ADRs (quando existir decisão arquitetural)

Nem todos precisam ser alterados em todas as entregas.

---

# 9. Git Workflow

Fluxo padrão:

```text
Nova funcionalidade

↓

Implementação

↓

Testes aprovados

↓

Documentação atualizada

↓

Git Commit
```

Commits devem representar uma unidade lógica de trabalho.

---

# 10. Checklist de Conclusão

Antes de considerar uma funcionalidade concluída, verificar:

- Código implementado.
- Ruff sem erros.
- Todos os testes aprovados.
- Tipagem correta.
- Docstrings adicionadas.
- Documentação atualizada.
- Estrutura do projeto preservada.

Somente após esse checklist a funcionalidade poderá ser considerada concluída.

---

# 11. Definition of Done

Uma funcionalidade é considerada pronta quando:

- atende aos requisitos funcionais;
- possui testes automatizados;
- não quebra funcionalidades existentes;
- segue os padrões arquiteturais do projeto;
- possui documentação atualizada;
- está apta para integração com os demais módulos.

---

# 12. Evolução do Processo

Este fluxo poderá evoluir conforme o projeto amadureça.

Entretanto, qualquer mudança significativa deverá preservar os princípios fundamentais do WINQuantLab:

- qualidade;
- simplicidade;
- reutilização;
- previsibilidade;
- evolução incremental.
