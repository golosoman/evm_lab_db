import json
from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import OrdersAPIErrors, ClientsAPIErrors, ProductAPIErrors
from collections import Counter

orders_api = Blueprint('orders_api', __name__, template_folder="templates", url_prefix='/api')


@orders_api.route("/get_order", methods=["GET"])
def get_order():
    data = request.args
    if 'id' in data:
        if int(data['id']) in unzipOneItem(dbHandler.execute(f"select id from orders")):
            res = dbHandler.execute(
                f"select orders.id, clients.name, product.name, brand_name, model, warranty_period, order_receipt_date, product.id from orders left join clients on clients_id = clients.id left join product on product_id = product.id left join brands on brands_id = brands.id where orders.id = {data['id']}")[
                0]
            return json.dumps({
                "id": res[0],
                "client_name": res[1],
                "product_name": res[2],
                "brand": res[3],
                'model': res[4],
                'warranty_period': str(res[5]),
                'order_receipt_date': str(res[6]),
                'product_id': res[7]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, OrdersAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute(
                "select orders.id, clients.name, product.name, brand_name, model, warranty_period, order_receipt_date, product_id from orders left join clients on clients_id = clients.id left join product on product_id = product.id left join brands on brands_id = brands.id"):
            print(item)
            res.append({
                "id": item[0],
                "client_name": item[1],
                "product_name": item[2],
                "brand": item[3],
                'model': item[4],
                'warranty_period': str(item[5]),
                'order_receipt_date': str(item[6]),
                "product_id": item[7]
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@orders_api.route("/add_order", methods=["POST"])
def add_order():
    data = request.json
    if Counter(['clients_id', 'product_id', 'order_receipt_date']) == Counter(list(data.keys())):
        if len(dbHandler.execute(f"select * from clients where id = {data['clients_id']}")) == 0:
            return abort(409, ClientsAPIErrors.idErr)
        if len(dbHandler.execute(f"select * from product where id = {data['product_id']}")) == 0:
            return abort(409, ProductAPIErrors.idErr)
        try:
            dbHandler.add('orders', ['clients_id', 'product_id', 'guaranty', 'order_receipt_date'],
                          [data['clients_id'], data['product_id'], 0, data['order_receipt_date']])
        except Exception as e:
            print(e)
            return abort(500, OrdersAPIErrors.errorOccurred)
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(403, OrdersAPIErrors.errorOccurred)


@orders_api.route("/edit_order", methods=["PATCH"])
def edit_order():
    data = request.json
    if Counter(['id', 'clients_id', 'product_id', 'order_receipt_date']) == Counter(list(data.keys())):
        if len(dbHandler.execute(f"select * from clients where id = {data['clients_id']}")) == 0:
            return abort(409, ClientsAPIErrors.idErr)
        if len(dbHandler.execute(f"select * from product where id = {data['product_id']}")) == 0:
            return abort(409, ProductAPIErrors.idErr)
        try:
            if len(dbHandler.execute(f"select * from orders where id = {data['id']}")) != 0:
                dbHandler.update("orders", ['clients_id', 'product_id', 'order_receipt_date'],
                                 [data['clients_id'], data['product_id'], data['order_receipt_date']], data['id'])
            else:
                return abort(409, OrdersAPIErrors.idErr)
        except ValueError as e:
            print(e)
            return abort(409, OrdersAPIErrors.colValLenErr)
    else:
        return abort(409, OrdersAPIErrors.errorOccurred)


@orders_api.route("/delete_order", methods=["POST"])
def delete_order():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from orders where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, OrdersAPIErrors.errorOccurred)
