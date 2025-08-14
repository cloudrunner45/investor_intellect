from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import LoginForm, RegisterForm
from .db_creation import (
    User_cred,
    User_notes,
    save_to_watchlist_db,
    get_user_watchlist,
    save_to_note_db,
    check_if_note_exist,
    remove_from_watchlist,
)
from . import db, login_manager

import os

stock_api_key = os.getenv("STOCK_API_KEY")

main_bp = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User_cred.query.get(int(user_id))


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User_cred(
            username=form.username.data,
            user_email=form.email.data,
            password_hash=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("register.html", form=form, stock_api_key=stock_api_key)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User_cred.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("main.dashboard"))
    return render_template("login.html", form=form, stock_api_key=stock_api_key)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", stock="SPY", stock_api_key=stock_api_key)


@main_bp.route("/dashboard/<stock>")
def dashboard_stock(stock):
    return render_template("dashboard.html", stock=stock, stock_api_key=stock_api_key)


@main_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main_bp.route("/add_watchlist", methods=["POST"])
def process():
    ticker = request.form.get("data")
    save_to_watchlist_db(ticker, current_user.id)
    return "added to watchlist"


@main_bp.route("/remove_watchlist", methods=["POST"])
def deprocess():
    ticker = request.form.get("data")
    remove_from_watchlist(ticker, current_user.id)
    return "removed from watchlist"


@main_bp.route("/display_watchlist", methods=["POST", "GET"])
def send_watchlist():
    user_watchlist = get_user_watchlist(current_user.id)
    return jsonify(user_watchlist)


@main_bp.route("/get_note", methods=["POST"])
def get_note():
    note = request.form.get("data")
    user_id = request.form.get("user")
    ticker = request.form.get("ticker")
    save_to_note_db(user_id, ticker, note)
    return "good"


@main_bp.route("/display_note", methods=["POST", "GET"])
def send_note():
    user_id = request.form.get("user")
    ticker = request.form.get("ticker")
    if check_if_note_exist(user_id, ticker):
        query_note = db.session.query(User_notes).filter(
            User_notes.user_id == user_id, User_notes.ticker == ticker
        ).first()
        return query_note.ticker_notes
    else:
        return ""


@main_bp.route("/")
def index():
    return render_template("index.html", stock_api_key=stock_api_key)
