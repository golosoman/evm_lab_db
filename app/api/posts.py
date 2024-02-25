import json
from app.mysqlConnector import dbHandler
from flask import request, Blueprint, abort
from app.functions import unzipOneItem
from app.api.ErrorMessages import PostsAPIErrors

posts_api = Blueprint('posts_api', __name__, template_folder="templates", url_prefix='/api')


@posts_api.route("/get_post", methods=["GET"])
def get_client():
    data = request.args
    if 'id' in data:
        if int(data['id']) in unzipOneItem(dbHandler.execute(f"select id from posts")):
            res = dbHandler.execute(f"select * from posts where id = {data['id']}")[0]
            return json.dumps({
                "id": res[0],
                "title": res[1]
            }), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, PostsAPIErrors.idErr)
    else:
        res = []
        for item in dbHandler.execute("select * from posts"):
            res.append({
                "id": item[0],
                "title": item[1]
            })
        return json.dumps(res), 200, {'Content-Type': 'application/json'}


@posts_api.route("/add_post", methods=["POST"])
def add_client():
    data = request.json
    if "title" in data:
        if data['title'].strip() not in unzipOneItem(dbHandler.execute("select title from posts")):
            try:
                dbHandler.add("posts", "title", data['title'].strip())
            except Exception as e:
                print(e)
                return abort(500, PostsAPIErrors.errorOccurred)
            return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
        else:
            return abort(409, PostsAPIErrors.idErr)
    else:
        return abort(403, PostsAPIErrors.errorOccurred)


@posts_api.route("/edit_post", methods=["PATCH"])
def edit_client():
    data = request.json
    if 'id' in data and 'title' in data:
        try:
            if len(dbHandler.execute(f"select * from posts where id = {data['id']}")) != 0 \
                    and data['title'].strip() not in unzipOneItem(dbHandler.execute("select title from posts")):
                dbHandler.update("posts", "title", data['title'], data['id'])
                return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
            else:
                return abort(409, PostsAPIErrors.idErr)
        except ValueError as e:
            print(e)
            return abort(409, PostsAPIErrors.colValLenErr)
    else:
        return abort(409, PostsAPIErrors.errorOccurred)


@posts_api.route("/delete_post", methods=["POST"])
def delete_post():
    data = request.json
    if 'id' in data:
        try:
            dbHandler.execute(f"delete from posts where id = {data['id']}")
        except Exception as e:
            return json.dumps({"success": "False"}), 200, {'Content-Type': 'application/json'}
        return json.dumps({"success": "True"}), 200, {'Content-Type': 'application/json'}
    else:
        return abort(409, PostsAPIErrors.errorOccurred)
