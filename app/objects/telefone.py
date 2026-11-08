import re


class Telefone:
    _DDDS_VALIDOS = {
        11, 12, 13, 14, 15, 16, 17, 18, 19,
        21, 22, 24, 27, 28,
        31, 32, 33, 34, 35, 37, 38,
        41, 42, 43, 44, 45, 46,
        47, 48, 49, 51, 53, 54, 55,
        61, 62, 63, 64, 65, 66, 67, 68, 69,
        71, 73, 74, 75, 77, 79,
        81, 82, 83, 84, 85, 86, 87, 88, 89,
        91, 92, 93, 94, 95, 96, 97, 98, 99,
    }

    def __init__(self, valor: str) -> None:
        normalizado = self.normalizar(valor)
        if not self._validar(normalizado):
            raise ValueError("Telefone brasileiro inválido.")
        self._valor = normalizado

    @staticmethod
    def normalizar(valor: object) -> str:
        return re.sub(r"\D", "", valor) if isinstance(valor, str) else ""

    @classmethod
    def _validar(cls, valor: str) -> bool:
        if len(valor) != 11 or len(set(valor)) == 1:
            return False
        if int(valor[:2]) not in cls._DDDS_VALIDOS:
            return False
        numero = valor[2:]
        return numero[0] == "9" and numero[1] != "0"

    @property
    def valor(self) -> str:
        return self._valor

    def formatado(self) -> str:
        ddd, numero = self._valor[:2], self._valor[2:]
        return f"({ddd}) {numero[:5]}-{numero[5:]}"

    def __str__(self) -> str:
        return self.formatado()

    def __repr__(self) -> str:
        return f"Telefone('{self._valor}')"
