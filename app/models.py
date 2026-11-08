from datetime import date, datetime, timezone
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Index
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuario"
    __table_args__ = (
        CheckConstraint("saldo >= 0", name="ck_usuario_saldo_nao_negativo"),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
        comment="Identificador único do usuário.",
    )
    nome = db.Column(
        String(100),
        nullable=False,
        comment="Nome completo normalizado do usuário.",
    )
    cpf = db.Column(
        String(11),
        nullable=False,
        unique=True,
        index=True,
        comment="CPF normalizado, sem pontuação, usado na autenticação.",
    )
    email = db.Column(
        String(254),
        nullable=False,
        unique=True,
        index=True,
        comment="Endereço de e-mail normalizado do usuário.",
    )
    telefone = db.Column(
        String(11),
        nullable=False,
        comment="Número de celular brasileiro normalizado, com DDD e sem pontuação.",
    )
    data_nascimento = db.Column(
        db.Date,
        nullable=False,
        comment="Data de nascimento do usuário maior de idade.",
    )
    senha = db.Column(
        String(60),
        nullable=False,
        comment="Hash BCrypt da senha do usuário.",
    )
    saldo = db.Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        comment="Saldo monetário atual da conta.",
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Data e hora de criação do usuário, armazenada em UTC.",
    )
    updated_at = db.Column(
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
    ) -> None:
        super().__init__()
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.senha = senha
        self.saldo = saldo

    transacoes_enviadas = relationship(
        "Transacao",
        foreign_keys="Transacao.conta_origem_id",
        back_populates="origem",
        passive_deletes=True,
    )
    transacoes_recebidas = relationship(
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

    id = db.Column(
        db.Integer,
        primary_key=True,
        comment="Identificador único da transação.",
    )
    conta_origem_id = db.Column(
        db.Integer,
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID do usuário que enviou o valor.",
    )
    conta_destino_id = db.Column(
        db.Integer,
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID do usuário que recebeu o valor.",
    )
    valor = db.Column(
        Numeric(12, 2),
        nullable=False,
        comment="Valor positivo transferido entre as contas.",
    )
    data_hora = db.Column(
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

    origem = relationship(
        "Usuario",
        foreign_keys=[conta_origem_id],
        back_populates="transacoes_enviadas",
    )
    destino = relationship(
        "Usuario",
        foreign_keys=[conta_destino_id],
        back_populates="transacoes_recebidas",
    )