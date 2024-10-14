import pytest
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza
from faker import Faker


class TestRestaurantPizza:
    '''Class RestaurantPizza in models.py'''

    def test_price_between_1_and_30(self):
        '''requires price between 1 and 30.'''

        with app.app_context():

            pizza = Pizza(
                name=Faker().name(), ingredients="Dough, Sauce, Cheese")
            restaurant = Restaurant(name=Faker().name(), address='Main St')
            db.session.add(pizza)
            db.session.add(restaurant)
            db.session.commit()

            restaurant_pizza_1 = RestaurantPizza(
                restaurant_id=restaurant.id, pizza_id=pizza.id, price=1)
            restaurant_pizza_2 = RestaurantPizza(
                restaurant_id=restaurant.id, pizza_id=pizza.id, price=30)
            db.session.add(restaurant_pizza_1)
            db.session.add(restaurant_pizza_2)
            db.session.commit()

    def test_price_too_low(self):
        '''requires price between 1 and 30 and fails when price is 0.'''

        with app.app_context():

            with pytest.raises(ValueError):
                pizza = Pizza(
                    name=Faker().name(), ingredients="Dough, Sauce, Cheese")
                restaurant = Restaurant(name=Faker().name(), address='Main St')
                db.session.add(pizza)
                db.session.add(restaurant)
                db.session.commit()

                restaurant_pizza = RestaurantPizza(
                    restaurant_id=restaurant.id, pizza_id=pizza.id, price=0)
                db.session.add(restaurant_pizza)
                db.session.commit()

    def test_price_too_high(self):
        '''requires price between 1 and 30 and fails when price is 31.'''

        with app.app_context():

            with pytest.raises(ValueError):
                pizza = Pizza(
                    name=Faker().name(), ingredients="Dough, Sauce, Cheese")
                restaurant = Restaurant(name=Faker().name(), address='Main St')
                db.session.add(pizza)
                db.session.add(restaurant)
                db.session.commit()

                restaurant_pizza = RestaurantPizza(
                    restaurant_id=restaurant.id, pizza_id=pizza.id, price=31)
                db.session.add(restaurant_pizza)
                db.session.commit()
