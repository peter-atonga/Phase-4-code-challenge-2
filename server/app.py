#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api=Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class Restarants(Resource):
    def get(self):
        restaurants=Restaurant.query.all()
        restaurants=[restaurant.to_dict() for restaurant in restaurants]
        restaurants1=[]
        for restaurant in restaurants:
            del restaurant["restaurant_pizzas"]
            restaurants1.append(restaurant)
        return make_response(restaurants1,200)
api.add_resource(Restarants,'/restaurants')

class Restaurant_by_id(Resource):
    def get(self,id):
        restaurant=Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return make_response({"error":"Restaurant not found"},404)
        restaurant=restaurant.to_dict()
        for pizza in restaurant["restaurant_pizzas"]:
            pizza["pizza"]=Pizza.query.filter_by(id=pizza['pizza_id']).first().to_dict()
        return make_response(restaurant,200)
    
    def delete(self,id):
        restaurant=Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return make_response({"error":"Restaurant not found"},404)
        db.session.delete(restaurant)
        db.session.commit()
        return make_response({"message":"Restaurant deleted successfully"},204)
api.add_resource(Restaurant_by_id,'/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        pizzas=Pizza.query.all()
        return make_response([pizza.to_dict() for pizza in pizzas],200)
    
api.add_resource(Pizzas,'/pizzas')

class RestaurantPizzas(Resource):
    def post(self):
        data=request.get_json()
        price=data['price']
        pizza_id=data['pizza_id']
        restaurant_id=data['restaurant_id']
        
        if 1<=price<=30:
            restaurant_pizza=RestaurantPizza(price=price,pizza_id=pizza_id,restaurant_id=restaurant_id)
            if restaurant_pizza:
                db.session.add(restaurant_pizza)
                db.session.commit()
                return make_response(restaurant_pizza.to_dict(),201)
        else:
            return make_response({"errors":["validation errors"]},400)
api.add_resource(RestaurantPizzas,'/restaurant_pizzas')
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)