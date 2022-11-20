from flask import Blueprint
from app.db import get_db
from flask import (Blueprint, request)

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.get("/<account_number>")
def get_account(account_number):
    sql = """SELECT a.account_number, c.name as customer_name, a.balance FROM account a JOIN customer c on a.customer_number = c.customer_number WHERE a.account_number = %s;"""

    db, cur = get_db()
    cur.execute(sql, (account_number,))
    account = cur.fetchone()
    if account is None:
        return {"message": "your account number is not found"}, 404
    return {"account_number": account[0], "customer_name": account[1], "balance": account[2]}


@bp.post("/<from_account_number>/transfer")
def transfer(from_account_number):
    sql = """SELECT a.account_number, c.name as customer_name, a.balance FROM account a JOIN customer c on a.customer_number = c.customer_number WHERE a.account_number = %s;"""
    db, cur = get_db()
    cur.execute(sql, (from_account_number,))
    account = cur.fetchone()

    data = request.data
    if not data:
        return {"message": "to_account_number, amount are required"}, 400

    req = request.get_json()
    to_account_number = None
    amount = None
    if not req:
        return {"message": "to_account_number, amount are required"}, 400

    if "to_account_number" not in req:
        return {"message": "to_account_number is required"}, 400
    to_account_number = req["to_account_number"]

    if "amount" not in req:
        return {"message": "amount is required"}, 400

    amount = req['amount']
    if type(amount) != int:
        return {"message": "amount must be numeric"}, 400

    if amount <= 0:
        return {"message": "amount must be more than 0"}, 400

    if amount > account[2]:
        return {"message": "insufficient funds"}, 400

    if type(to_account_number) == int:
        to_account_number = str(to_account_number)

    if from_account_number == to_account_number:
        return {"message": "can't self transfer"}, 400

    sql = "SELECT account_number FROM account WHERE account_number = %s;"
    db, cur = get_db()
    cur.execute(sql, (from_account_number,))
    account = cur.fetchone()
    if account is None:
        return {"message": "from_account_number not found"}, 404

    sql = "SELECT account_number FROM account WHERE account_number = %s;"
    cur.execute(sql, (to_account_number,))
    account = cur.fetchone()
    if account is None:
        return {"message": "to_account_number not found"}, 404

    sql = "UPDATE account SET balance = balance - %s WHERE account_number = %s;"
    cur.execute(sql, (amount, from_account_number,))

    sql = "UPDATE account SET balance = balance + %s WHERE account_number = %s;"
    cur.execute(sql, (amount, to_account_number,))
    return "", 201
