from faker import Faker
from random import choices, randint


from app import app
from models import db, Restaurant, RestaurantPizza, Pizza


fake = Faker()

def seed_data():
    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()

    restaurants = []
    pizzas = []
    restaurant_pizzas = []
    ingredients = ['cheese', 'pepperoni', 'sausage', 'onions', 'peppers', 'black olives', 'ham', 'pineapple', 'anchovies', 'basil']

    for _ in range(15):
        pizza = Pizza(
            name=fake.first_name(),
            ingredients=', '.join(choices(ingredients, k=3))
        )
        pizzas.append(pizza)
    
    for _ in range(5):
        restaurant = Restaurant(
            name=fake.company(),
            address=fake.address()
        )
        restaurants.append(restaurant)
    
    for restaurant in restaurants:
        rand_pizzas = choices(pizzas, k=randint(3, 5))
        for pizza in rand_pizzas:
            rp = RestaurantPizza(
                price=randint(10, 25)
            )
            rp.pizza = pizza
            rp.restaurant = restaurant
            restaurant_pizzas.append(rp)
    
    db.session.add_all(restaurants + pizzas + restaurant_pizzas)
    db.session.commit()


if __name__ == '__main__':
    app.run(port=3000)
