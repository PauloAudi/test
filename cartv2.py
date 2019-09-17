import json
import os
import random

from flask import Flask, request
from flask_restful import Api, Resource
from tinydb import TinyDB, where

DBG = True
app = Flask(__name__)
api = Api(app)

# DB setup
wd = os.getcwd() + '/db.json'
db = TinyDB(wd)
carts_db = db.table("carts")
items_db = db.table("items")


class Item:
    def __init__(self, id, cart_id, product, qtd):
        self.id = id
        self.cart_id = cart_id
        self.product = product
        self.qtd = qtd


class Cart:
    def __init__(self, id, items=[]):
        self.id = id
        self.items = items


def convert_to_json(entry):
    if entry:
        return json.loads(json.dumps(entry, default=lambda input: input.__dict__))


class CartResource(Resource):

    @app.route('/carts', methods=['POST'])
    def post_empty_cart():
        id = random.randint(1, 100)
        cart = Cart(id)
        data = convert_to_json(cart)
        carts_db.insert(data)
        if DBG:
            print("POST: {}".format(data))
        return data, 201

    @app.route('/carts/<int:id>/items', methods=['POST'])
    def post_item_to_cart(id):
        items_json = request.get_json()
        cart = carts_db.search(where('id') == id)
        if cart and cart != []:
            product = items_json['product']
            qtd = items_json['qtd']
            if product != "" and qtd > 0:
                same_product = items_db.search((where('product') == product) & (where('cart_id') == id))
                if same_product and same_product != []:
                    same_product2 = same_product.pop()
                    qtd2 = same_product2['qtd']
                    item_id = same_product2['id']
                    qtd3 = qtd + qtd2
                    items_db.remove((where('product') == product) & (where('cart_id') == id))
                    item = Item(item_id, id, product, qtd3)
                    data = convert_to_json(item)
                    items_db.insert(data)
                else:
                    item_id = random.randint(1, 100)
                    item = Item(item_id, id, product, qtd)
                    data = convert_to_json(item)
                    items_db.insert(data)
                return data, 201
            else:
                return "Check if Product is empty or quantity is more then 1", 400
        else:
            return "Cart ID: {} - Not found".format(id), 404

    @app.route('/carts/<int:id>', methods=['GET'])
    def get_cart(id):
        items = items_db.search(where('cart_id') == int(id))
        if items and items != []:
            if DBG:
                print("GET: ", items)
            cart = Cart(id, items)
            data = convert_to_json(cart)
            return data, 200
        else:
            return "Cart not found", 404

    @app.route('/carts/<int:id>/items/<int:item_id>', methods=['DELETE'])
    def delete(id, item_id):
        cart = carts_db.search(where('id') == id)
        if cart and cart != []:
            item = items_db.search((where('cart_id') == id) & (where('id') == item_id))
            if item and item != []:
                items_db.remove((where('cart_id') == id) & (where('id') == item_id))
                return {}, 200
            else:
                return "Item ID: {} Not Found".format(item_id), 404
        else:
            return "Cart ID: {} Not Found".format(item_id), 404


api.add_resource(CartResource, "/cart")

if __name__ == '__main__':
    app.run(debug=True)