import json
from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import ClientsAPIErrors

clients_api = Blueprint('clients_api', __name__, template_folder="templates", url_prefix='/api')


@clients_api.route("/get_client", methods=["GET"])
def get_client():
    data = request.args
    print(data, list(data.keys()))
    if 'id' in data:
        if int(data['id']) in unzipOneItem(dbHandler.execute(f"select id from clients")):
            res = dbHandler.execute(f"select * from clients where id = {data['id']}")[0]
            print(res)
            return json.dumps({
                "id": res[0],
                "name": res[1],
                "phoneNumber": res[2]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, ClientsAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute("select * from clients"):
            res.append({
                "id": item[0],
                "name": item[1],
                "phoneNumber": item[2]
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@clients_api.route("/add_client", methods=["POST"])
def add_client():
    data = request.json
    if "name" in data and 'phoneNumber' in data:
        # if data['name'].strip() not in unzipOneItem(dbHandler.execute("select name from clients")):
        try:
            dbHandler.add("clients", ["name", "phoneNumber"], [data['name'].strip(), data['phoneNumber'].strip()])
        except Exception as e:
            print(e)
            return abort(500, ClientsAPIErrors.errorOccurred)
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
        # else:
        #     return
    else:
        return abort(403, ClientsAPIErrors.errorOccurred)


@clients_api.route("/edit_client", methods=["PATCH"])
def edit_client():
    data = request.json
    if 'id' in data and 'name' in data and 'phoneNumber' in data:
        try:
            if len(dbHandler.execute(f"select * from clients where id = {data['id']}")) != 0:
                dbHandler.update("clients", ["name", 'phoneNumber'],
                                 [data['name'].strip(), data['phoneNumber'].strip()], data['id'])
                return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
            else:
                return abort(409, ClientsAPIErrors.idErr)
        except ValueError as e:
            print(e)
            return abort(409, ClientsAPIErrors.colValLenErr)
    else:
        return abort(409, ClientsAPIErrors.errorOccurred)


@clients_api.route("/delete_client", methods=["POST"])
def delete_client():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from clients where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, ClientsAPIErrors.errorOccurred)
