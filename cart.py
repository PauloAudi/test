from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

carts = []

items = []

class Cart(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("items")
        args = parser.parse_args()

        cart = {
            "id": args["id"],
            "items": args["items"],
        }
        carts.append(cart)
        return cart, 201
        
    def get(self):
        for cart in carts:
            if(id == carts["id"]):
                return cart, 200
        return "Cart not found", 404

        
api.add_resource(Cart, "/carts")

app.run()
    
