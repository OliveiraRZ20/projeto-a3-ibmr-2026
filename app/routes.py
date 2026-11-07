from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .models import Transacao, Usuario, db
from .services import create_user, normalize_cpf, transfer_money, verify_password


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


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

    @app.get("/dashboard")
    @login_required
    def dashboard():
        user = db.session.get(Usuario, session["user_id"])
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