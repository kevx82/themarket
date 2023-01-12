import pandas as pd
import numpy as np
from products import Products

class Customer:

    def __init__(self, tm, entry, timestamp) -> None:
        """"
        Initiate the Customer
        """"
        self.tm = tm
        self.destination = self.tm.columns
        self.location = self.next_location(self.destination, entry)

        self.shopping_cart = []
        self.stolen_article = []
        self.transition = []
        self.move(timestamp)
        self.prd = Products()

    def next_location(self, probs):
        new_location = np.random.choice(self.destination, p=probs)

    def move(self, timestamp):
        """"
        Moves the customer to a random location
        """"
        probs = tm[tm.index == self.location].values[0] # da es ein doppelarray ist, möchte ich den 1. bekommen
        new_location = self.next_location(destination, probs)

        if new_location != self.location:
            self.transition.append({timestamp:new_location})
        self.location = new_location


    def pick_product(self):
        """"
        Picks a random product
        """"
        department_products = self.prd.shopping_department[self.location]
        product_choice = np.random.choice(list(department_products.keys()))
        self.buy_or_steal()

    def buy_or_steal(self, product, price):
        """"
        Buy or steal product and add them to the corresponding list
        """"
        if np.random.uniform() > 0.8:
            print(f"The customer stole {product}.")
            self.stolen_article = self.stolen_article.append({product:price})
        else: 
            print(f"The customer add {product} to the shopping cart.")
            self.shopping_cart = self.shopping_cart.append({product:price})
