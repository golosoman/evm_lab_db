import json
from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import TypesOfRepairsAPIErrors

types_of_repairs_api = Blueprint('types_of_repairs_api', __name__, template_folder="templates", url_prefix='/api')


@types_of_repairs_api.route("/get_types_of_repairs", methods=["GET"])
def get_types():
    data = request.args
    if "id" in data:
        if int(data['id']) in unzipOneItem(dbHandler.execute(f"select id from types_of_repairs")):
            res = dbHandler.execute(f"select * from types_of_repairs where id = {data['id']}")[0]
            return json.dumps({
                "id": res[0],
                "desc": res[1]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, TypesOfRepairsAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute("select * from types_of_repairs"):
            res.append({
                "id": item[0],
                "desc": item[1]
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@types_of_repairs_api.route("/get_type_by_desc", methods=["GET"])
def get_type_by_desc():
    data = request.args
    if 'description' in data:
        res = dbHandler.execute(f"select * from types_of_repairs where description = '{data['description']}'")
        if len(res) != 0:
            return json.dumps({
                "id": res[0][0],
                "desc": res[0][1]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, TypesOfRepairsAPIErrors.errorOccurred)
    else:
        return abort(409, TypesOfRepairsAPIErrors.errorOccurred)


@types_of_repairs_api.route("/add_types_of_repairs", methods=["POST"])
def add_types():
    data = request.json
    if "description" in data:
        if data['description'].strip() not in unzipOneItem(
                dbHandler.execute("select description from types_of_repairs")):
            try:
                dbHandler.add("types_of_repairs", "description", data['description'].strip())
            except Exception as e:
                print(e)
                return abort(500, "Произошла ошибка")
            return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, TypesOfRepairsAPIErrors.nameUsedErr)
    else:
        return abort(403, "Произошла ошибка")


@types_of_repairs_api.route("/edit_types_of_repairs", methods=["PATCH"])
def edit_types():
    data = request.json
    if 'id' in data and 'description' in data:
        try:
            if len(dbHandler.execute(
                    f"select * from types_of_repairs where description = '{data['description'].strip()}'")) == 0:
                if len(dbHandler.execute(f"select * from types_of_repairs where id = {data['id']}")) != 0:
                    dbHandler.update("types_of_repairs", "description", data['description'].strip(), data['id'])
                    return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
                else:
                    return abort(409, TypesOfRepairsAPIErrors.idErr)
            else:
                return abort(409, TypesOfRepairsAPIErrors.nameUsedErr)
        except ValueError as e:
            print(e)
            return abort(409, TypesOfRepairsAPIErrors.colValLenErr)
    else:
        return abort(409, TypesOfRepairsAPIErrors.errorOccurred)


@types_of_repairs_api.route("/delete_types_of_repairs", methods=["POST"])
def delete_order():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from types_of_repairs where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, TypesOfRepairsAPIErrors.errorOccurred)
