# ADR-003 — Organização modular dos indicadores técnicos

## Status

Aceito.

## Data

05/08/2026.

## Contexto

O WINQuantLab começou sua camada de indicadores técnicos com a implementação da
Média Móvel Simples — SMA.

Inicialmente, seria possível concentrar diferentes médias móveis em um único
arquivo, como:

```text
indicators/
└── moving_average.py
