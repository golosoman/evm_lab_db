import json
from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import ExecutionOfOrdersAPIErrors, OrdersAPIErrors, TypesOfRepairsAPIErrors
from collections import Counter

execution_api = Blueprint('execution_api', __name__, template_folder="templates", url_prefix='/api')


@execution_api.route('/get_execution', methods=["GET"])
def get_execution():
    data = request.args
    if "id" in data:
        if len(dbHandler.execute(f"select * from execution_of_orders where id = {data['id']}")) != 0:
            res = dbHandler.execute(
                f"select execution_of_orders.id, clients.name, product.warranty_period, types_of_repairs.description, repair_cost, order_execution_date, message, date_of_receipt, orders.order_receipt_date, orders.id from execution_of_orders left join orders on order_id = orders.id left join clients on orders.clients_id = clients.id left join product on orders.product_id = product.id left join types_of_repairs on execution_of_orders.types_of_repairs_id = types_of_repairs.id where execution_of_orders.id = {data['id']}")[
                0]
            print(res)
            return json.dumps({
                "id": res[0],
                "client_name": res[1],
                "warranty_period": str(res[2]),
                "repair_type": res[3],
                "repair_cost": res[4],
                "order_execution_date": str(res[5]),
                "message": res[6],
                "date_of_receipt": str(res[7]),
                "order_receipt_date": str(res[8]),
                "order_id": res[9]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, ExecutionOfOrdersAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute(
                "select execution_of_orders.id, clients.name, product.warranty_period, types_of_repairs.description, repair_cost, order_execution_date, message, date_of_receipt, orders.order_receipt_date, orders.id from execution_of_orders left join orders on order_id = orders.id left join clients on orders.clients_id = clients.id left join product on orders.product_id = product.id left join types_of_repairs on execution_of_orders.types_of_repairs_id = types_of_repairs.id"):
            res.append({
                "id": item[0],
                "client_name": item[1],
                "warranty_period": str(item[2]),
                "repair_type": item[3],
                "repair_cost": item[4],
                "order_execution_date": str(item[5]),
                "message": item[6],
                "date_of_receipt": str(item[7]),
                "order_receipt_date": str(item[8]),
                "order_id": item[9]
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@execution_api.route("/add_execution", methods=["POST"])
def add_execution():
    data = request.json
    if Counter(['order_id', 'types_of_repairs_id', 'repair_cost', 'order_execution_date', 'message', 'date_of_receipt',
                'amount_of_payment']) == Counter(list(data.keys())):
        if len(dbHandler.execute(f"select * from orders where id = {data['order_id']}")) == 0:
            return abort(409, OrdersAPIErrors.idErr)
        if len(dbHandler.execute(f"select * from types_of_repairs where id = {data['types_of_repairs_id']}")) == 0:
            return abort(409, TypesOfRepairsAPIErrors.idErr)
        try:
            dbHandler.add("execution_of_orders",
                          ['order_id', 'types_of_repairs_id', 'repair_cost', 'order_execution_date', 'message',
                           'date_of_receipt', 'amount_of_payment'],
                          [data['order_id'], data['types_of_repairs_id'], data['repair_cost'],
                           data['order_execution_date'], data['message'], data['date_of_receipt'],
                           data['amount_of_payment']])
            return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
        except Exception as e:
            print(e)
            return abort(500, ExecutionOfOrdersAPIErrors.errorOccurred)
    else:
        return abort(403, ExecutionOfOrdersAPIErrors.errorOccurred)


@execution_api.route("/edit_execution", methods=["PATCH"])
def edit_execution():
    data = request.json
    if Counter(['id', 'order_id', 'types_of_repairs_id', 'repair_cost', 'order_execution_date', 'message',
                'date_of_receipt']) == Counter(list(data.keys())):
        if len(dbHandler.execute(f"select * from orders where id = {data['order_id']}")) == 0:
            return abort(409, OrdersAPIErrors.idErr)
        if len(dbHandler.execute(f"select * from types_of_repairs where id = {data['types_of_repairs_id']}")) == 0:
            return abort(409, TypesOfRepairsAPIErrors.idErr)
        if len(dbHandler.execute(f"select * from execution_of_orders where id = {data['id']}")) == 0:
            return abort(409, ExecutionOfOrdersAPIErrors.idErr)
        try:
            dbHandler.update("execution_of_orders",
                             ['order_id', 'types_of_repairs_id', 'repair_cost', 'order_execution_date', 'message',
                              'date_of_receipt'],
                             [data['order_id'], data['types_of_repairs_id'], data['repair_cost'],
                              data['order_execution_date'], data['message'], data['date_of_receipt']],
                             data['id'])
            return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
        except ValueError as e:
            print(e)
            return abort(409, ExecutionOfOrdersAPIErrors.colValLenErr)
    else:
        return abort(409, ExecutionOfOrdersAPIErrors.errorOccurred)


@execution_api.route("/delete_execution", methods=["POST"])
def delete_execution():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from execution_of_orders where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, ExecutionOfOrdersAPIErrors.errorOccurred)
