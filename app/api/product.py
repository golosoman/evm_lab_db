import json
from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import ProductAPIErrors
from collections import Counter

product_api = Blueprint('product_api', __name__, template_folder="templates", url_prefix='/api')


@product_api.route("/get_product", methods=["GET"])
def get_client():
    data = request.args
    if 'id' in data:
        if int(data['id']) in unzipOneItem(dbHandler.execute(f"select id from product")):
            res = dbHandler.execute(f"select product.id, name, brand_name, model, technical_specifications, "
                                    f"warranty_period from product left join brands on brands_id = brand"
                                    f"s.id where product.id = {data['id']}")[0]
            return json.dumps({
                "id": res[0],
                "name": res[1],
                "brand_name": res[2],
                "model": res[3],
                "technical_specifications": res[4],
                "warranty_period": str(res[5])
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, ProductAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute(f"select product.id, name, brand_name, model, technical_specifications, "
                                      f"warranty_period from product left join brands on brands_id = brand"
                                      f"s.id"):
            res.append({
                "id": item[0],
                "name": item[1],
                "brand_name": item[2],
                "model": item[3],
                "technical_specifications": item[4],
                "warranty_period": str(item[5])
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@product_api.route("/add_product", methods=["POST"])
def add_client():
    data = request.json
    if Counter(['name', 'brands_id', 'model', 'technical_specification', 'warranty_period']) == Counter(
            list(data.keys())):
        try:
            dbHandler.add("product", ['name', 'brands_id', 'model', 'technical_specifications', 'warranty_period'],
                          [data['name'].strip(), data['brands_id'], data['model'].strip(),
                           data['technical_specification'], data['warranty_period']])
        except Exception as e:
            print(e)
            return abort(500, ProductAPIErrors.errorOccurred)
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(403, ProductAPIErrors.errorOccurred)


@product_api.route("/edit_product", methods=["PATCH"])
def edit_client():
    data = request.json
    if Counter(['id', 'name', 'brands_id', 'model', 'technical_specification', 'warranty_period']) == Counter(
            list(data.keys())):
        try:
            if len(dbHandler.execute(f"select * from product where id = {data['id']}")) != 0:
                dbHandler.update("product",
                                 ['name', 'brands_id', 'model', 'technical_specifications', 'warranty_period'],
                                 [data['name'], data['brands_id'], data['model'], data['technical_specification'],
                                  data['warranty_period']], data['id'])
                return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
            else:
                return abort(409, ProductAPIErrors.idErr)
        except ValueError as e:
            print(e)
            return abort(409, ProductAPIErrors.colValLenErr)
    else:
        return abort(409, ProductAPIErrors.errorOccurred)


@product_api.route("/delete_product", methods=["POST"])
def delete_product():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from product where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, ProductAPIErrors.errorOccurred)
