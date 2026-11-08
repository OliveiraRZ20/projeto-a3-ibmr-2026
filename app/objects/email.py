import re


class Email:
    _PATTERN = re.compile(
        r"^[A-Za-z0-9]+(?:[._%+-][A-Za-z0-9]+)*@"
        r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
        r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
    )

    def __init__(self, valor: str) -> None:
        normalizado = self.normalizar(valor)
        if not self._PATTERN.fullmatch(normalizado) or len(normalizado) > 254:
            raise ValueError("E-mail inválido.")
        self._valor = normalizado

    @staticmethod
    def normalizar(valor: object) -> str:
        return valor.strip().lower() if isinstance(valor, str) else ""

    @property
    def valor(self) -> str:
        return self._valor

    def __str__(self) -> str:
        return self._valor

    def __repr__(self) -> str:
        return f"Email('{self._valor}')"
