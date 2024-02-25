import json

from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import BrandsAPIErrors
from collections import Counter

report_api = Blueprint('report_api', __name__, template_folder="templates", url_prefix='/api')


@report_api.route('/get_report', methods=["GET"])
def get_report():
    data = request.args
    if Counter(['month', 'year']) == Counter(list(data.keys())):
        res = []
        for item in dbHandler.execute(
                f"select order_id, clients.name, clients.phoneNumber, order_receipt_date, order_execution_date, product.name, brands.brand_name, product.model, product.warranty_period from execution_of_orders left join orders on order_id = orders.id left join clients on orders.clients_id = clients.id left join product on orders.product_id = product.id left join brands on product.brands_id = brands.id where month(order_execution_date) = {data['month']} and year(order_execution_date) = {data['year']} order by product.model"):
            res.append({
                "id": item[0],
                "client_name": item[1],
                "phoneNumber": item[2],
                "order_receipt_date": str(item[3]),
                "order_execution_date": str(item[4]),
                "product_name": item[5],
                "brand_name": item[6],
                "model": item[7],
                "warranty_period": str(item[8])
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, BrandsAPIErrors.errorOccurred)
