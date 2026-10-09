"""
Excepciones personalizadas de TechCovers.
"""


class ErrorTechCovers(Exception):
    """Excepción base para errores propios de TechCovers."""


class StockInsuficienteError(ErrorTechCovers):
    """Se produce cuando no hay stock suficiente para una operación."""