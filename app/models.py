from datetime import datetime, timezone
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

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(String(100), nullable=False)
    cpf = db.Column(String(11), nullable=False, unique=True, index=True)
    senha = db.Column(String(60), nullable=False)
    saldo = db.Column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))

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

    id = db.Column(db.Integer, primary_key=True)
    conta_origem_id = db.Column(
        db.Integer,
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False,
    )
    conta_destino_id = db.Column(
        db.Integer,
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False,
    )
    valor = db.Column(Numeric(12, 2), nullable=False)
    data_hora = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

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