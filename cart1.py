from builtins import list

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from tinydb import TinyDB, Query, where
from tinydb.operations import delete
import os


class Cart(Resource):

    def post(self, id):
        items_json = request.get_json()
        value = carts.search(where('id') == id)
        if not value:
            value = {
                "id": id,
                "items": items_json
            }
            carts.insert(value)
            if DBG:
                print("POST: {}".format(value))
            return value, 201
        else:
            return "ID: {} already exists in DB, change ID".format(id), 500
        
    def get(self, id):
        value = carts.search(where('id') == id)
        if value:
            if DBG:
                print("GET: ", value)
            return value, 200
        else:
            return "Cart not found", 404

    def put(self, id):
        items_json = request.get_json()
        value = carts.search(where('id') == id)
        if not value:
            value = {
                "id": id,
                "items": items_json
            }
            carts.insert(value)
            if DBG:
                print("PUT: {}".format(value))
            return value, 201
        else:
            value = {
                "id": id,
                "items": items_json
            }
            carts.update(value, where('id') == id)
            if DBG:
                print("PUT: {}".format(value))
        return value, 201

    def delete(self, id):
        value = carts.search(where('id') == id)
        if not value:
            return "ID: {} not present".format(id), 404
        else:
            carts.update(delete('id'), where('id') == id)
            return "ID: {} was deleted".format(id), 200


DBG = True
wd = os.getcwd() + '/db.json'
db = TinyDB(wd)
carts = db.table("carts")
cart_query = Query()

if __name__ == '__main__':

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Cart, "/carts/<string:id>")
    app.run(debug = True)
