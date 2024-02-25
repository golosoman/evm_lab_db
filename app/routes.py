import flask

from app import app
from app.mysqlConnector import dbHandler
from flask import render_template, request, redirect, url_for, make_response


# Функция вывода страницы с ошибкой 404, если она не найдена
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>Страница не найдена</h1><p>Попробуйте другой запрос</p>", 404


# Функция вывода страны с ошибкой 500 по вине сервера
@app.errorhandler(500)
def page_not_found(e):
    return "<h1>Ошибка на стороне сервера</h1><p>Сообщите в тех. поддержку</p>", 500


@app.route("/", methods=["GET"])
@app.route("/table_data", methods=["GET"])
def table_data():
    return render_template("table_data.html")


@app.route("/table_execute_orders", methods=["GET"])
def table_execute_orders():
    return render_template("table_execute_orders.html")


@app.route("/table_staff", methods=["GET"])
def main_page():
    print(dbHandler.test())
    return render_template("table_staff.html")


@app.route("/order_form", methods=["GET"])
def order_form():
    return render_template("order_form.html")


@app.route("/execute_order_form", methods=["GET"])
def execute_order_form():
    return render_template("execute_order_form.html")


@app.route("/add_staff_form", methods=["GET"])
def add_staff():
    return render_template("add_staff_form.html")


@app.route("/edit_data_order_table", methods=["GET"])
def edit_data_order_table():
    return render_template("edit_data_order_table.html")


@app.route("/edit_execute_orders", methods=["GET"])
def edit_execute_orders():
    return render_template("edit_execute_orders.html")


@app.route("/edit_staff", methods=['GET'])
def edit_staff():
    return render_template("edit_staff.html")


@app.route("/test", methods=["GET"])
def test():
    return render_template("temp.html")


@app.route("/report_table", methods=['GET'])
def report_table():
    data = request.args
    if len(data) == 0:
        return render_template("report_table.html")
    else:
        return render_template("test_report_table.html")
