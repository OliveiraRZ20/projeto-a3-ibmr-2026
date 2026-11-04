class CPF():
    def __init__(self, valor: str) -> None:
        valor_normalizado = self.normalizar(valor)
        if not self._validar(valor_normalizado):
            raise ValueError(f"CPF inválido: '{valor}'")
        self._valor: str = valor_normalizado

    @staticmethod
    def normalizar(valor: object) -> str:
        """Retorna o CPF sem pontuação para validação e persistência."""
        if not isinstance(valor, str):
            return ""
        return valor.replace(".", "").replace("-", "").strip()

    @property
    def valor(self) -> str:
        return self._valor

    @classmethod
    def _validar(cls, valor: object) -> bool:
        # vamos pensar em um input com somente números
        # valida que é string
        if not isinstance(valor, str):
            return False
        # valida que tem somente números
        if not valor.isdigit():
            return False
        # valida que tem o tamanho correto
        if len(valor) != 11:
            return False
        # valida que não é sequência direta
        if len(set(valor)) == 1:
            return False
        # valida primeiro dígito verificador
        if not cls.validar_decimo_digito(valor):
            return False
        # valida segundo dígito verificador
        if not cls.validar_decimo_primeiro_digito(valor):
            return False
        return True

    @staticmethod
    def validar_decimo_digito(cpf: str) -> bool:
        multiplicacoes: list[int] = list(range(10, 1, -1))
        resultado: int = sum(int(cpf[i]) * multiplicacoes[i] for i in range(9)) % 11
        decimo_digito: int = 0 if resultado < 2 else 11 - resultado
        return decimo_digito == int(cpf[-2])

    @staticmethod
    def validar_decimo_primeiro_digito(cpf: str) -> bool:
        multiplicacoes: list[int] = list(range(11, 1, -1))
        resultado: int = sum(int(cpf[i]) * multiplicacoes[i] for i in range(10)) % 11
        decimo_primeiro_digito: int = 0 if resultado < 2 else 11 - resultado
        return decimo_primeiro_digito == int(cpf[-1])

    def __str__(self) -> str:
        v = self._valor
        return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}"

    def __repr__(self) -> str:
        return f"CPF('{self._valor}')"


def main() -> None:
    # Teste de Instanciação Válida
    try:
        cpf_valido = CPF("21618722735")
        print(f"Formatado (__str__):     {cpf_valido}")
        print(f"Representação (__repr__): {repr(cpf_valido)}")
        print(f"Propriedade .valor:       {cpf_valido.valor}")
    except ValueError as e:
        print(e)

    print("-" * 40)

    # Teste de Instanciação Inválida (Lança Exceção)
    try:
        cpf_invalido = CPF("12345678901")
        print(cpf_invalido)
    except ValueError as e:
        print(f"Sucesso ao capturar erro esperado: {e}")


if __name__ == "__main__":
    main()
