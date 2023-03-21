from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DATETIME, ForeignKey,CheckConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()

class PizzaError(Exception):
    pass
class RestaurantError(Exception):
    pass

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    def to_dict_summary(self):
        rest_dict = {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }
        return rest_dict
    
    def to_dict(self):
        pizzas = [pizza.to_dict_summary() for pizza in self.restaurants]
        rest_dict = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "pizzas": pizzas
            # "pizzas": [pizza.to_dict_summary() for pizza in RestaurantPizza.query.filter(RestaurantPizza.restaurant_id == self.id).all()]

        }

        return rest_dict


    restaurants = db.relationship("RestaurantPizza", back_populates="restaurant")

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DATETIME)
    updated_at = db.Column(db.DATETIME)

    def to_dict(self):
        pizza_dict = {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
        }   

        return pizza_dict  
    
    pizzas = db.relationship("RestaurantPizza", back_populates="pizza")

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    price = db.Column(db.Integer, db.CheckConstraint("price > 0 AND price < 31"))
    created_at = db.Column(db.DATETIME)
    updated_at = db.Column(db.DATETIME)
    
    def to_dict_summary(self):
        pizza = Pizza.query.filter(Pizza.id == self.pizza_id).first()
        pizza_dict = {
            "id": self.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients,
        }

        return pizza_dict
    
    pizza = db.relationship("Pizza", back_populates="pizzas")
    restaurant = db.relationship("Restaurant", back_populates="restaurants")
    
    # @validates("pizza_id")
    # def validate_pizza(self,key,pizza_id):
    #     if pizza_id not in [pizza.id for pizza in Pizza.query.all()]:
    #         raise PizzaError("Pizza does not exist")
    #     return pizza_id
    
    # @validates("restaurant_id")
    # def validate_restaurant(self,key,restaurant_id):
    #     if restaurant_id not in [restaurant.id for restaurant in Restaurant.query.all()]:
    #         raise RestaurantError("Restaurant does not exist")
    #     return restaurant_id

    # @validates("restaurant_pizzas.price")
    # def validate_price(self,key,price):
    #     if not 0 < price < 31:
    #         raise ValueError("Price out of range")
        
    #     new_pizza = RestaurantPizza(
    #         rest


    