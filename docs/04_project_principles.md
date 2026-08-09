# WINQuantLab

> Biblioteca Python para pesquisa quantitativa aplicada ao mercado financeiro.

---

# Documento

Project Principles

Versão: 1.0

Status: Em desenvolvimento

Última atualização: 2026-08-07

---

# 1. Objetivo

Este documento registra os princípios que orientam todas as decisões técnicas do WINQuantLab.

Eles servem como referência para garantir consistência durante a evolução da biblioteca, independentemente da quantidade de funcionalidades implementadas.

Sempre que existir dúvida sobre uma decisão de arquitetura, implementação ou organização, estes princípios deverão ser considerados antes da escrita de qualquer código.

---

# 2. Arquitetura Antes da Implementação

Toda funcionalidade deve começar pela compreensão do problema.

Antes de escrever código, deve existir uma arquitetura capaz de suportar a solução de forma simples, reutilizável e escalável.

O objetivo é reduzir retrabalho e evitar refatorações desnecessárias.

---

# 3. Simplicidade Acima da Complexidade

A solução mais simples que atende corretamente ao problema deve ser a escolhida.

Complexidade somente será introduzida quando existir uma necessidade real.

Código simples é mais fácil de entender, testar, manter e evoluir.

---

# 4. Reutilização Acima da Duplicação

Sempre que possível, funcionalidades comuns devem ser reutilizadas.

Entretanto, abstrações prematuras devem ser evitadas.

Uma função somente deverá ser promovida para um nível superior quando existir reutilização comprovada.

---

# 5. Testes Fazem Parte da Funcionalidade

Uma funcionalidade somente é considerada concluída quando possui testes automatizados.

Os testes não são documentação complementar.

Eles fazem parte da implementação.

---

# 6. Refatoração Guiada por Necessidade

Refatorações não devem ocorrer apenas por preferência pessoal.

Elas devem possuir uma justificativa objetiva.

Exemplos:

- correção de bugs;
- reutilização por múltiplos módulos;
- melhoria arquitetural significativa;
- simplificação comprovada.

Mudanças puramente estéticas deverão ser evitadas durante o desenvolvimento de uma funcionalidade.

---

# 7. Responsabilidade Única

Cada módulo deverá possuir uma responsabilidade claramente definida.

Exemplos:

- Loader importa dados.
- Validator valida dados.
- Normalizer padroniza dados.
- Indicadores calculam indicadores.
- Estratégias tomam decisões.
- Backtesting executa simulações.
- Analytics calcula métricas.
- Reports exporta resultados.

Essa separação reduz acoplamento e facilita manutenção.

---

# 8. Evolução Incremental

O projeto deverá evoluir em pequenas etapas.

Grandes mudanças deverão ser divididas em funcionalidades menores.

Cada evolução deverá manter a biblioteca funcional e estável.

---

# 9. APIs Estáveis

Interfaces públicas deverão permanecer estáveis sempre que possível.

Mudanças incompatíveis deverão ocorrer apenas quando realmente necessárias e deverão ser documentadas.

O objetivo é preservar a compatibilidade entre versões.

---

# 10. Documentação é Parte do Código

Toda funcionalidade implementada deverá possuir documentação compatível com seu estado atual.

A documentação deve evoluir junto com o código.

Documentação desatualizada é considerada um defeito do projeto.

---

# 11. Dados Antes de Opiniões

O WINQuantLab existe para validar hipóteses quantitativas.

Nenhuma estratégia deve ser considerada boa ou ruim sem evidências produzidas por testes e métricas.

Decisões devem ser baseadas em dados, não em percepções.

---

# 12. Aprendizado Contínuo

O projeto possui também um objetivo educacional.

Cada módulo deve ser escrito de forma clara, organizada e compreensível, permitindo que novos desenvolvedores entendam facilmente seu funcionamento.

A legibilidade do código é considerada um requisito de qualidade.

---

# 13. Melhoria Contínua

A arquitetura do WINQuantLab deverá evoluir continuamente.

Entretanto, toda evolução deverá preservar os princípios definidos neste documento.

O crescimento da biblioteca nunca deverá comprometer sua organização, previsibilidade e facilidade de manutenção.
