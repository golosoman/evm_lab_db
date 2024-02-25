from flask import Flask
from config import DB_NAME, DB_PASSWORD
from app.mysqlConnector import DataBaseHandler
from app.api.brands import brands_api
from app.api.clients import clients_api
from app.api.execution_of_orders import execution_api
from app.api.orders import orders_api
from app.api.performers import performers_api
from app.api.posts import posts_api
from app.api.product import product_api
from app.api.staff import staff_api
from app.api.types_of_repairs import types_of_repairs_api
from app.api.report import report_api

app = Flask(__name__, static_folder="static")

from app import routes

dbHandler = DataBaseHandler(DB_NAME, DB_PASSWORD)
dbHandler.loadDump()

app.register_blueprint(brands_api)
app.register_blueprint(clients_api)
app.register_blueprint(execution_api)
app.register_blueprint(orders_api)
app.register_blueprint(performers_api)
app.register_blueprint(posts_api)
app.register_blueprint(product_api)
app.register_blueprint(staff_api)
app.register_blueprint(types_of_repairs_api)
app.register_blueprint(report_api)

app.run(debug=True)
