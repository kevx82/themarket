import logging

import pandas as pd
import numpy as np
#from products import Products

class Customer:

    def __init__(self, tm, entry, customer_no) -> None:
        """
        Initiate the Customer
        """
        self.tm = tm
        self.entry = entry
        self.customer_no = customer_no

        self.destination = self.tm.columns.to_list()
        self.location = self.next_location(self.entry)

        self.shopping_cart = []
        self.stolen_article = []
        # dict for all transitions
        self.transition = {'timestamp': [], 'location': [], 'customer_no': []}

        #self.prd = Products()

    def next_location(self, probs):
         return np.random.choice(self.destination, p=probs)

    def add_transition(self, timestamp):
        self.transition['timestamp'].append(timestamp)
        self.transition['location'].append(self.location)
        self.transition['customer_no'].append(self.customer_no)

    def move(self, timestamp):
        """
        Moves the customer to a random location
        """
        # getting probabilities for destinations of current location
        # da es ein doppelarray ist, möchte ich den 1. bekommen
        probs = self.tm[self.tm.index == self.location].values[0]
        # setting possible new location
        new_location = self.next_location(probs)

         # checking for new location
        if new_location != self.location:
            # changing current position to new location
            self.location = new_location

            # adding new position to transition list
            self.add_transition(timestamp)
        
'''
    def pick_product(self):
        """
        Picks a random product
        """
        department_products = self.prd.shopping_department[self.location]
        product_choice = np.random.choice(list(department_products.keys()))
        self.buy_or_steal()

    def buy_or_steal(self, product, price):
        """
        Buy or steal product and add them to the corresponding list
        """
        if np.random.uniform() > 0.8:
            print(f"The customer stole {product}.")
            self.stolen_article = self.stolen_article.append({product:price})
        else: 
            print(f"The customer add {product} to the shopping cart.")
            self.shopping_cart = self.shopping_cart.append({product:price})
'''