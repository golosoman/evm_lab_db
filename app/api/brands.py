import json

import flask
import mysql.connector.errors

from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import BrandsAPIErrors

brands_api = Blueprint('brands_api', __name__, template_folder="templates", url_prefix='/api')


@brands_api.route("/get_brands", methods=["GET"])
def get_brands():
    data = request.args
    if "id" in data:
        if int(data['id']) in unzipOneItem(dbHandler.execute(f"select id from brands")):
            res = dbHandler.execute(f"select * from brands where id = {data['id']}")[0]
            return json.dumps({
                "id": res[0],
                "name": res[1]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, BrandsAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute("select * from brands"):
            res.append({
                "id": item[0],
                "name": item[1]
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@brands_api.route("/add_brand", methods=["POST"])
def add_brand():
    data = request.json
    if "brand_name" in data:
        if data['brand_name'].strip() not in unzipOneItem(dbHandler.execute("select brand_name from brands")):
            try:
                dbHandler.add("brands", "brand_name", data['brand_name'].strip())
            except Exception as e:
                print(e)
                return abort(500, "Произошла ошибка")
            return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, BrandsAPIErrors.nameUsedErr)
    else:
        return abort(403, "Произошла ошибка")


@brands_api.route("/edit_brand", methods=["PATCH"])
def edit_brand():
    data = request.json
    if 'id' in data and 'brand_name' in data:
        try:
            if len(dbHandler.execute(f"select * from brands where brand_name = '{data['brand_name'].strip()}'")) == 0:
                if len(dbHandler.execute(f"select * from brands where id = {data['id']}")) != 0:
                    dbHandler.update("brands", "brand_name", data['brand_name'].strip(), data['id'])
                    return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
                else:
                    return abort(409, BrandsAPIErrors.idErr)
            else:
                return abort(409, BrandsAPIErrors.nameUsedErr)
        except ValueError as e:
            print(e)
            return abort(409, BrandsAPIErrors.colValLenErr)
    else:
        return abort(409, BrandsAPIErrors.errorOccurred)


@brands_api.route("/delete_brand", methods=["POST"])
def delete_brand():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from brands where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, BrandsAPIErrors.errorOccurred)
