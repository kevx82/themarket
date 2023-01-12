import pandas as pd
import numpy as np
from products import Products

class Customer:

    def __init__(self, location, shopping_cart, stolen_article) -> None:
        """"
        Initiate the Customer
        """"
        self.location = location
        self.shopping_cart = shopping_cart
        self.stolen_article = stolen_article
        self.prd = Products()

    def move(self):
        """"
        Moves the customer to a random location
        """"
        new_location = 
        location = new_location


    def pick_product(self):
        """"
        Picks a random product
        """"
        department_products = self.prd.shopping_department[self.location]
        product_choice = np.random.choice(list(department_products.keys()))
        self.buy_or_steal()

    def buy_or_steal(self, product, price):
        """"
        Buy or steal product and save it
        """"
        if np.random.uniform() > 0.8:
            print(f"The customer stole {product}.")
            self.stolen_article = self.stolen_article.append({product:price})
        else: 
            print(f"The customer add {product} to the shopping cart.")
            self.shopping_cart = self.shopping_cart.append({product:price})
