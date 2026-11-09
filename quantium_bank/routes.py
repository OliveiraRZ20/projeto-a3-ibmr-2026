from functools import wraps
from datetime import datetime, time
from decimal import Decimal, InvalidOperation

from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .models import Transacao, Usuario, db
from .services import create_user, normalize_cpf, transfer_money, verify_password


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id is None or db.session.get(Usuario, user_id) is None:
            session.clear()
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        user = db.session.get(Usuario, session["user_id"])
        if user is None or not user.is_admin:
            flash("Acesso restrito a administradores.", "error")
            return redirect(url_for("dashboard"))
        return view(*args, **kwargs)

    return wrapped


def _parse_filter_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.combine(
            datetime.strptime(value, "%Y-%m-%d").date(),
            time.min,
        )
    except ValueError:
        raise ValueError("Data de filtro inválida.")


def _parse_required_filter_date(value: str) -> datetime:
    parsed = _parse_filter_date(value)
    if parsed is None:
        raise ValueError("Data de filtro inválida.")
    return parsed


def register_routes(app: Flask) -> None:
    @app.get("/")
    def index():
        return redirect(url_for("dashboard" if "user_id" in session else "login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if "user_id" in session:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            try:
                user = Usuario.query.filter_by(
                    cpf=normalize_cpf(request.form.get("cpf", ""))
                ).first()
            except ValueError:
                user = None
            if user is None:
                flash("CPF não encontrado.", "error")
            elif not verify_password(request.form.get("senha", ""), user.senha):
                flash("Senha incorreta.", "error")
            else:
                session.clear()
                session["user_id"] = user.id
                session["is_admin"] = user.is_admin
                return redirect(url_for("dashboard"))
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if "user_id" in session:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            try:
                create_user(
                    request.form.get("nome", ""),
                    request.form.get("cpf", ""),
                    request.form.get("senha", ""),
                    email=request.form.get("email", ""),
                    telefone=request.form.get("telefone", ""),
                    data_nascimento=request.form.get("data_nascimento", ""),
                    confirmacao_senha=request.form.get("confirmacao_senha", ""),
                )
                db.session.commit()
                flash("Cadastro realizado com sucesso.", "success")
                return redirect(url_for("login"))
            except (ValueError, IntegrityError) as error:
                db.session.rollback()
                message = getattr(error, "orig", error)
                flash(str(message), "error")
            except SQLAlchemyError:
                db.session.rollback()
                flash("Não foi possível concluir o cadastro.", "error")
        return render_template("register.html")

    @app.get("/perfil")
    @login_required
    def perfil():
        user = db.session.get(Usuario, session["user_id"])
        if user is None:
            session.clear()
            return redirect(url_for("login"))
        return render_template("perfil.html", user=user)

    @app.get("/dashboard")
    @login_required
    def dashboard():
        user = db.session.get(Usuario, session["user_id"])
        if user is None:
            session.clear()
            return redirect(url_for("login"))
        transactions = Transacao.query.filter(
            (Transacao.conta_origem_id == user.id)
            | (Transacao.conta_destino_id == user.id)
        ).order_by(Transacao.data_hora.desc()).limit(20).all()
        return render_template("dashboard.html", user=user, transactions=transactions)

    @app.get("/usuarios")
    @login_required
    def usuarios():
        page = request.args.get("page", 1, type=int)
        pagination = Usuario.query.order_by(Usuario.nome).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template("usuarios.html", pagination=pagination)

    @app.get("/admin")
    @admin_required
    def admin_dashboard():
        total_users = db.session.scalar(
            db.select(func.count()).select_from(Usuario)
        )
        total_admins = db.session.scalar(
            db.select(func.count()).select_from(Usuario).where(Usuario.is_admin.is_(True))
        )
        total_balance = db.session.scalar(
            db.select(func.coalesce(func.sum(Usuario.saldo), 0))
        )
        total_transactions = db.session.scalar(
            db.select(func.count()).select_from(Transacao)
        )
        total_transferred = db.session.scalar(
            db.select(func.coalesce(func.sum(Transacao.valor), 0))
        )
        recent_users = Usuario.query.order_by(Usuario.created_at.desc()).limit(5).all()
        return render_template(
            "admin_dashboard.html",
            total_users=total_users,
            total_admins=total_admins,
            total_balance=total_balance,
            total_transactions=total_transactions,
            total_transferred=total_transferred,
            recent_users=recent_users,
        )

    @app.get("/admin/usuarios")
    @admin_required
    def admin_usuarios():
        page = request.args.get("page", 1, type=int)
        search = request.args.get("q", "").strip()
        query = Usuario.query
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Usuario.nome.ilike(pattern),
                    Usuario.cpf.ilike(pattern),
                    Usuario.email.ilike(pattern),
                )
            )
        if request.args.get("admin") == "true":
            query = query.filter(Usuario.is_admin.is_(True))
        try:
            if request.args.get("desde"):
                query = query.filter(
                    Usuario.created_at
                    >= _parse_required_filter_date(request.args["desde"])
                )
            if request.args.get("ate"):
                query = query.filter(
                    Usuario.created_at
                    < _parse_required_filter_date(request.args["ate"]).replace(
                        hour=23, minute=59, second=59
                    )
                )
        except ValueError as error:
            flash(str(error), "error")
        pagination = query.order_by(Usuario.nome).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template(
            "admin_usuarios.html",
            pagination=pagination,
            search=search,
            desde=request.args.get("desde", ""),
            ate=request.args.get("ate", ""),
        )

    @app.get("/admin/transacoes")
    @admin_required
    def admin_transacoes():
        page = request.args.get("page", 1, type=int)
        cpf = request.args.get("cpf", "").strip()
        query = Transacao.query
        if cpf:
            pattern = f"%{cpf}%"
            query = query.filter(
                or_(
                    Transacao.origem.has(Usuario.cpf.ilike(pattern)),
                    Transacao.destino.has(Usuario.cpf.ilike(pattern)),
                )
            )
        minimum = request.args.get("minimo", "").strip()
        maximum = request.args.get("maximo", "").strip()
        try:
            if minimum:
                query = query.filter(Transacao.valor >= Decimal(minimum))
            if maximum:
                query = query.filter(Transacao.valor <= Decimal(maximum))
        except (InvalidOperation, ValueError):
            flash("Faixa de valor inválida.", "error")
        try:
            if request.args.get("desde"):
                query = query.filter(
                    Transacao.data_hora
                    >= _parse_required_filter_date(request.args["desde"])
                )
            if request.args.get("ate"):
                query = query.filter(
                    Transacao.data_hora
                    < _parse_required_filter_date(request.args["ate"]).replace(
                        hour=23, minute=59, second=59
                    )
                )
        except ValueError as error:
            flash(str(error), "error")
        pagination = query.order_by(Transacao.data_hora.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template(
            "admin_transacoes.html",
            pagination=pagination,
            cpf=cpf,
            minimo=minimum,
            maximo=maximum,
            desde=request.args.get("desde", ""),
            ate=request.args.get("ate", ""),
        )

    @app.route("/transferir", methods=["GET", "POST"])
    @login_required
    def transferir():
        if request.method == "POST":
            try:
                transfer_money(
                    session["user_id"],
                    request.form.get("cpf_destino", ""),
                    request.form.get("valor", ""),
                )
                db.session.commit()
                flash("Transferência realizada com sucesso.", "success")
                return redirect(url_for("dashboard"))
            except (ValueError, IntegrityError) as error:
                db.session.rollback()
                message = getattr(error, "orig", error)
                flash(str(message), "error")
            except SQLAlchemyError:
                db.session.rollback()
                flash("Não foi possível concluir a transferência.", "error")
        return render_template("transferir.html")

    @app.post("/logout")
    def logout():
        session.clear()
        flash("Sessão encerrada.", "success")
        return redirect(url_for("login"))