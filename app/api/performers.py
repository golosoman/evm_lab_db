import json
from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import ExecutionOfOrdersAPIErrors, PerformersAPIErrors, StaffAPIErrors
from collections import Counter

performers_api = Blueprint('performers_api', __name__, template_folder="templates", url_prefix='/api')


@performers_api.route("/get_performer", methods=["GET"])
def get_performers():
    data = request.args
    if 'id' in data:
        if len(dbHandler.execute(f"select * from performers where id = {data['id']}")) != 0:
            res = dbHandler.execute(
                f"select performers.id, clients.name, product.warranty_period, types_of_repairs.description, repair_cost, order_execution_date, message, date_of_receipt, staff.name, posts.title from performers left join execution_of_orders on execution_of_orders_id = execution_of_orders.id left join staff on staff_id = staff.id left join posts on posts_id = posts.id left join orders on order_id = orders.id left join clients on orders.clients_id = clients.id left join product on orders.product_id = product.id left join types_of_repairs on execution_of_orders.types_of_repairs_id = types_of_repairs.id where id = {data['id']}")
            return json.dumps({
                "id": res[0],
                "client_name": res[1],
                "warranty_period": res[2],
                "repair_type": res[3],
                "repair_cost": res[4],
                "order_execution_date": res[5],
                "message": res[6],
                "date_of_receipt": res[7],
                "staff_name": res[8],
                "post_title": res[9]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, PerformersAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute(
                "select performers.id, clients.name, product.warranty_period, types_of_repairs.description, repair_cost, order_execution_date, message, date_of_receipt, staff.name, posts.title from performers left join execution_of_orders on execution_of_orders_id = execution_of_orders.id left join staff on staff_id = staff.id left join posts on posts_id = posts.id left join orders on order_id = orders.id left join clients on orders.clients_id = clients.id left join product on orders.product_id = product.id left join types_of_repairs on execution_of_orders.types_of_repairs_id = types_of_repairs.id"):
            res.append({
                "id": item[0],
                "client_name": item[1],
                "warranty_period": item[2],
                "repair_type": item[3],
                "repair_cost": item[4],
                "order_execution_date": item[5],
                "message": item[6],
                "date_of_receipt": item[7],
                "staff_name": item[8],
                "post_title": item[9]
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@performers_api.route("/get_performer_by_execution", methods=["GET"])
def get_performer_by_execution():
    data = request.args
    if "id" in data:
        res = dbHandler.execute(f"select * from performers where execution_of_orders_id = {data['id']}")
        if len(res) != 0:
            return json.dumps({
                "id": res[0][0],
                "execution_of_orders_id": res[0][1],
                "staff_id": res[0][2]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, PerformersAPIErrors.errorOccurred)
    else:
        return abort(409, PerformersAPIErrors.errorOccurred)


@performers_api.route("/add_performer", methods=["POST"])
def add_performer():
    data = request.json
    if "execution_of_orders_id" in data and "staff_id" in data:
        if len(dbHandler.execute(
                f"select * from execution_of_orders where id = {data['execution_of_orders_id']}")) == 0:
            return abort(409, ExecutionOfOrdersAPIErrors.idErr)
        if len(dbHandler.execute(f"select * from staff where id = {data['staff_id']}")) == 0:
            return abort(409, StaffAPIErrors.idErr)
        try:
            dbHandler.add("performers", ['execution_of_orders_id', 'staff_id'],
                          [data['execution_of_orders_id'], data['staff_id']])
        except Exception as e:
            print(e)
            return abort(500, PerformersAPIErrors.errorOccurred)
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(403, PerformersAPIErrors.errorOccurred)


@performers_api.route("/edit_performer", methods=["PATCH"])
def edit_performers():
    data = request.json
    if 'id' in data and "execution_of_orders_id" in data and "staff_id" in data:
        if len(dbHandler.execute(
                f"select * from execution_of_orders where id = {data['execution_of_orders_id']}")) == 0:
            return abort(409, ExecutionOfOrdersAPIErrors.idErr)
        if len(dbHandler.execute(f"select * from staff where id = {data['staff_id']}")) == 0:
            return abort(409, StaffAPIErrors.idErr)
        if len(dbHandler.execute(f"select * from performers where id = {data['id']}")) == 0:
            return abort(409, PerformersAPIErrors.errorOccurred)
        try:
            dbHandler.update("performers", ["execution_of_orders_id", "staff_id"],
                             [data["execution_of_orders_id"], data["staff_id"]],
                             data['id'])
        except ValueError as e:
            print(e)
            return abort(409, PerformersAPIErrors.colValLenErr)
    else:
        return abort(409, PerformersAPIErrors.errorOccurred)


@performers_api.route("/delete_performer", methods=["POST"])
def delete_brand():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from performers where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, PerformersAPIErrors.errorOccurred)
