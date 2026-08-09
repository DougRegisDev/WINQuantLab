"""
Mapeamento oficial das colunas suportadas pelo WINQuantLab.
"""

COLUMN_MAPPING = {
    # Data
    "Data": "date",
    "Date": "date",

    # Hora
    "Hora": "time",
    "Time": "time",

    # Abertura
    "Abertura": "open",
    "Open": "open",

    # Máxima
    "Máxima": "high",
    "Maxima": "high",
    "High": "high",

    # Mínima
    "Mínima": "low",
    "Minima": "low",
    "Low": "low",

    # Fechamento
    "Fechamento": "close",
    "Close": "close",

    # Volume
    "Volume": "volume",
    "Tick Volume": "volume",
}
