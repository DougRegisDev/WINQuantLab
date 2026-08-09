# Guia de Contribuição

Antes de contribuir com o WINQuantLab, leia este documento.

Ele define o fluxo oficial de desenvolvimento utilizado no projeto e garante que toda nova funcionalidade mantenha o mesmo padrão de qualidade.

---

# Objetivo

O WINQuantLab é desenvolvido priorizando:

- simplicidade;
- organização;
- testes automatizados;
- documentação;
- arquitetura modular;
- evolução incremental.

Toda contribuição deve seguir esses princípios.

---

# Fluxo Oficial de Desenvolvimento

Toda nova funcionalidade deverá seguir o seguinte fluxo:

```
Planejamento
      ↓
Implementação
      ↓
Testes
      ↓
Refatoração
      ↓
Documentação
      ↓
Versionamento
```

Nenhuma etapa deve ser ignorada.

---

# Planejamento

Antes de escrever código é necessário definir:

- objetivo;
- arquitetura;
- responsabilidades;
- impacto na estrutura existente.

Sempre que houver uma decisão arquitetural relevante deverá ser criado um ADR.

---

# Implementação

Durante a implementação:

- manter responsabilidade única;
- evitar duplicação;
- reutilizar componentes existentes;
- seguir os padrões definidos em `coding_standards.md`.

Cada módulo deve possuir uma responsabilidade bem definida.

---

# Testes

Toda funcionalidade nova deve possuir testes automatizados.

Sempre que possível:

- testar comportamento esperado;
- testar erros;
- testar casos extremos;
- manter testes independentes.

Nenhuma funcionalidade é considerada concluída sem testes.

---

# Refatoração

Após a implementação, o código deverá ser revisado.

Perguntas importantes:

- existe duplicação?
- existe melhor organização?
- alguma função pode ser reutilizada?
- a arquitetura continua simples?

A refatoração nunca deve alterar o comportamento esperado.

---

# Documentação

Após a implementação devem ser atualizados, quando necessário:

- README.md
- CHANGELOG.md
- Roadmap
- Glossário
- ADR
- Architecture

A documentação faz parte da entrega.

---

# Versionamento

O projeto utiliza Semantic Versioning.

Formato:

```
MAJOR.MINOR.PATCH
```

Exemplo:

```
0.6.0
0.6.1
0.7.0
1.0.0
```

---

# Estrutura do Projeto

Cada módulo deve permanecer em sua responsabilidade.

Exemplo:

```
config/

core/

data/

indicators/

reports/

strategies/

tests/
```

Evite criar módulos genéricos.

---

# API Pública

Os usuários da biblioteca devem utilizar apenas a API pública.

Exemplo:

```python
from indicators.moving_averages import sma
```

Evite expor módulos internos desnecessariamente.

---

# Testes Obrigatórios

Antes de qualquer commit executar:

```bash
python -m pytest
```

Todos os testes devem permanecer aprovados.

---

# Verificação de Código

Executar:

```bash
python -m ruff check .
```

Nenhum aviso deve permanecer sem justificativa.

---

# Dependências

Novas bibliotecas somente deverão ser adicionadas quando:

- resolverem um problema real;
- reduzirem complexidade;
- forem amplamente utilizadas pela comunidade Python.

Toda nova dependência deverá ser adicionada em:

- requirements.txt
- pyproject.toml

quando aplicável.

---

# Organização dos Commits

Sempre que possível, cada commit deve representar uma única mudança lógica.

Exemplos:

- Implementação da SMA
- Implementação da EMA
- Refatoração das validações
- Atualização da documentação

Evite misturar várias alterações independentes em um único commit.

---

# Pull Requests

Cada Pull Request deve:

- possuir objetivo claro;
- manter todos os testes aprovados;
- atualizar a documentação quando necessário;
- respeitar os padrões definidos pelo projeto.

---

# Filosofia

O WINQuantLab adota uma filosofia de desenvolvimento incremental.

Antes de adicionar novas funcionalidades, garantir que a base atual esteja sólida.

A prioridade é:

1. Fazer funcionar.
2. Fazer corretamente.
3. Fazer de forma reutilizável.
4. Otimizar quando necessário.

---

# Checklist

Antes de finalizar qualquer funcionalidade confirme:

- [ ] Código implementado.
- [ ] Testes criados.
- [ ] Todos os testes aprovados.
- [ ] Ruff executado.
- [ ] Docstrings adicionadas.
- [ ] Type Hints adicionados.
- [ ] Documentação atualizada.
- [ ] CHANGELOG atualizado.
- [ ] Roadmap atualizado (quando necessário).
- [ ] ADR criado (quando necessário).

---

# Objetivo Final

O objetivo do WINQuantLab é evoluir para uma biblioteca quantitativa profissional, mantendo qualidade, previsibilidade e facilidade de manutenção em todas as etapas do desenvolvimento.

Cada contribuição deve aproximar o projeto desse objetivo.
