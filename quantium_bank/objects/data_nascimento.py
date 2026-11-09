from datetime import date, datetime


class DataNascimento:
    def __init__(self, valor: date | str) -> None:
        data = self._parse(valor)
        if data > date.today():
            raise ValueError("A data de nascimento não pode ser futura.")
        self._valor = data
        if self.idade_em(date.today()) < 18:
            raise ValueError("É necessário ter pelo menos 18 anos.")

    @staticmethod
    def _parse(valor: date | str) -> date:
        if isinstance(valor, datetime):
            return valor.date()
        if isinstance(valor, date):
            return valor
        if isinstance(valor, str):
            try:
                return date.fromisoformat(valor.strip())
            except ValueError:
                pass
        raise ValueError("Data de nascimento inválida.")

    def idade_em(self, referencia: date) -> int:
        idade = referencia.year - self._valor.year
        if (referencia.month, referencia.day) < (self._valor.month, self._valor.day):
            idade -= 1
        return idade

    @property
    def valor(self) -> date:
        return self._valor

    def __str__(self) -> str:
        return self._valor.strftime("%d/%m/%Y")

    def __repr__(self) -> str:
        return f"DataNascimento('{self._valor.isoformat()}')"
