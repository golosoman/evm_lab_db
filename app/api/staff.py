import json
from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import StaffAPIErrors
from collections import Counter

staff_api = Blueprint('staff_api', __name__, template_folder="templates", url_prefix='/api')


@staff_api.route("/get_staff", methods=["GET"])
def get_staff():
    data = request.args
    if "id" in data:
        if int(data['id']) in unzipOneItem(dbHandler.execute(f"select id from staff")):
            res = dbHandler.execute(
                f"select staff.id, name, title from staff left join posts on posts_id = posts.id where staff.id = {data['id']}")[
                0]
            return json.dumps({
                "id": res[0],
                "name": res[1],
                "title": res[2]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, StaffAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute("select staff.id, name, title from staff left join posts on posts_id = posts.id"):
            res.append({
                "id": item[0],
                "name": item[1],
                "title": item[2]
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@staff_api.route("/add_staff", methods=["POST"])
def add_staff():
    data = request.json
    print(data)
    if Counter(['name', 'posts_id']) == Counter(list(data.keys())):
        # try:
        dbHandler.add("staff", ["name", 'posts_id'], [data['name'].strip(), data['posts_id']])
        # except Exception as e:
        #     print(e.args)
        #     return abort(500, "Произошла ошибка")
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(403, "Произошла ошибка")


@staff_api.route("/edit_staff", methods=["PATCH"])
def edit_staff():
    data = request.json
    if Counter(['id', 'name', 'posts_id']) == Counter(list(data.keys())):
        try:
            if len(dbHandler.execute(f"select * from staff where id = {data['id']}")) != 0:
                dbHandler.update("staff", ["name", 'posts_id'], [data['name'].strip(), data['posts_id']], data['id'])
                return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
            else:
                return abort(409, StaffAPIErrors.idErr)
        except ValueError as e:
            print(e)
            return abort(409, StaffAPIErrors.colValLenErr)
    else:
        return abort(409, StaffAPIErrors.errorOccurred)


@staff_api.route("/delete_staff", methods=["POST"])
def delete_order():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from staff where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, StaffAPIErrors.errorOccurred)
