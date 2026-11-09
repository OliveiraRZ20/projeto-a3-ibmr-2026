from datetime import date, datetime, timezone
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuario"
    __table_args__ = (
        CheckConstraint("saldo >= 0", name="ck_usuario_saldo_nao_negativo"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        comment="Identificador único do usuário.",
    )
    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nome completo normalizado do usuário.",
    )
    cpf: Mapped[str] = mapped_column(
        String(11),
        nullable=False,
        unique=True,
        index=True,
        comment="CPF normalizado, sem pontuação, usado na autenticação.",
    )
    email: Mapped[str] = mapped_column(
        String(254),
        nullable=False,
        unique=True,
        index=True,
        comment="Endereço de e-mail normalizado do usuário.",
    )
    telefone: Mapped[str] = mapped_column(
        String(11),
        nullable=False,
        comment="Número de celular brasileiro normalizado, com DDD e sem pontuação.",
    )
    data_nascimento: Mapped[date] = mapped_column(
        nullable=False,
        comment="Data de nascimento do usuário maior de idade.",
    )
    senha: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        comment="Hash BCrypt da senha do usuário.",
    )
    is_admin: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        comment="Indica se o usuário pode consultar o painel administrativo.",
    )
    saldo: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        comment="Saldo monetário atual da conta.",
    )
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Data e hora de criação do usuário, armazenada em UTC.",
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Data e hora da última atualização, armazenada em UTC.",
    )

    def __init__(
        self,
        *,
        nome: str,
        cpf: str,
        email: str,
        telefone: str,
        data_nascimento: date,
        senha: str,
        saldo: Decimal = Decimal("0.00"),
        is_admin: bool = False,
    ) -> None:
        super().__init__()
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.senha = senha
        self.saldo = saldo
        self.is_admin = is_admin

    transacoes_enviadas: Mapped[list["Transacao"]] = relationship(
        "Transacao",
        foreign_keys="Transacao.conta_origem_id",
        back_populates="origem",
        passive_deletes=True,
    )
    transacoes_recebidas: Mapped[list["Transacao"]] = relationship(
        "Transacao",
        foreign_keys="Transacao.conta_destino_id",
        back_populates="destino",
        passive_deletes=True,
    )


class Transacao(db.Model):
    __tablename__ = "transacao"
    __table_args__ = (
        CheckConstraint("valor > 0", name="ck_transacao_valor_positivo"),
        CheckConstraint(
            "conta_origem_id != conta_destino_id",
            name="ck_transacao_contas_diferentes",
        ),
        Index("ix_transacao_origem", "conta_origem_id"),
        Index("ix_transacao_destino", "conta_destino_id"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        comment="Identificador único da transação.",
    )
    conta_origem_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID do usuário que enviou o valor.",
    )
    conta_destino_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID do usuário que recebeu o valor.",
    )
    valor: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        comment="Valor positivo transferido entre as contas.",
    )
    data_hora: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Data e hora da transferência, armazenada em UTC.",
    )

    def __init__(
        self,
        *,
        conta_origem_id: int,
        conta_destino_id: int,
        valor: Decimal,
    ) -> None:
        super().__init__()
        self.conta_origem_id = conta_origem_id
        self.conta_destino_id = conta_destino_id
        self.valor = valor

    origem: Mapped["Usuario"] = relationship(
        "Usuario",
        foreign_keys=[conta_origem_id],
        back_populates="transacoes_enviadas",
    )
    destino: Mapped["Usuario"] = relationship(
        "Usuario",
        foreign_keys=[conta_destino_id],
        back_populates="transacoes_recebidas",
    )