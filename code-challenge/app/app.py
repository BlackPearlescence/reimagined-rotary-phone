#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from json import dumps
from sqlalchemy.exc import IntegrityError

from models import db, Restaurant, Pizza, RestaurantPizza, PizzaError,RestaurantError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return 'Pizza-Restaurant RESTFUL API homepage'

@app.route('/restaurants')
def restaurants():
    rest_list = []
    for restaurant in Restaurant.query.all():
        # rest = {
        #     "id": restaurant.id,
        #     "name": restaurant.name,
        #     "address": restaurant.address
        # }
        rest_list.append(restaurant.to_dict_summary())

    return make_response(jsonify(rest_list),200)

@app.route('/restaurants/<int:id>', methods = ["GET","DELETE"])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if restaurant == None:
        return make_response(
            {"error":"Restaurant not found"},
            404)
    
    if request.method == "GET":
        restaurant_dict = restaurant.to_dict()
        return make_response(jsonify(restaurant_dict),200)
    elif request.method == "DELETE":
        restaurant_pizzas = RestaurantPizza.query.filter(RestaurantPizza.restaurant_id == id).all()
        # Delete restaurant pizzas
        for rest_pizza in restaurant_pizzas:
            db.session.delete(rest_pizza)
        db.session.commit()

        # Delete the restaurant
        db.session.delete(restaurant)
        db.session.commit()
        return make_response("",200)
        

@app.route('/pizzas')
def pizzas():
    pizza_list = []
    for pizza in Pizza.query.all():
        pizza_list.append(pizza.to_dict())

    return make_response(jsonify(pizza_list),200)

@app.route('/restaurant_pizzas', methods = ["GET","POST"])
def restaurant_pizzas():
    if request.method == "POST":
        new_pizza = RestaurantPizza(
            price = request.json["price"],
            pizza_id = request.json["pizza_id"],
            restaurant_id = request.json["restaurant_id"]
        )
        validation_errors = []
        if new_pizza.pizza_id not in [pizza.id for pizza in Pizza.query.all()]:
            validation_errors.append("Pizza does not exist")
        if new_pizza.restaurant_id not in [restaurant.id for restaurant in Restaurant.query.all()]:
            validation_errors.append("Restaurant does not exist")
        if len(validation_errors) == 0:
            db.session.add(new_pizza)
            db.session.commit()
            return make_response(jsonify(new_pizza.to_dict_summary()),200)
        else:
            return make_response(jsonify({"errors": validation_errors}),403)
            


        # pizza = Pizza.query.filter(Pizza.id == new_pizza.pizza_id).first()
        # pizza_dict = pizza.to_dict()



if __name__ == '__main__':
    app.run(port=3000)
