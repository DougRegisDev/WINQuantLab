# ADR-002 — Introdução do Normalizer

## Status

Aceita

---

## Contexto

O projeto WINQuantLab deverá importar dados provenientes de diferentes plataformas de negociação.

Cada plataforma utiliza convenções próprias para nomear colunas e representar datas, horários e preços.

Permitir que os módulos seguintes tratem essas diferenças aumentaria o acoplamento e dificultaria a manutenção.

---

## Decisão

Introduzir um módulo chamado `Normalizer`, responsável por converter qualquer conjunto de dados aceito para um formato interno único.

Formato oficial:

- datetime
- open
- high
- low
- close
- volume

Após essa etapa, nenhum outro módulo deverá depender do formato original do arquivo importado.

---

## Consequências

### Positivas

- Redução do acoplamento entre módulos.
- Facilidade para adicionar novas fontes de dados.
- Indicadores e estratégias trabalham sempre com o mesmo esquema.
- Testes mais simples.

### Negativas

- Inclusão de uma etapa adicional no pipeline de importação.
- Necessidade de manter um mapeamento de colunas para diferentes plataformas.