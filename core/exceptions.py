class WINQuantError(Exception):
    """
    Classe base para todas as exceções do projeto.
    """


class DataLoaderError(WINQuantError):
    """
    Erros relacionados ao carregamento de dados.
    """


class FileValidationError(DataLoaderError):
    """
    Arquivo inválido.
    """


class MissingColumnError(DataLoaderError):
    """
    Coluna obrigatória ausente.
    """


class InvalidDataTypeError(DataLoaderError):
    """
    Tipo de dado inválido.
    """
