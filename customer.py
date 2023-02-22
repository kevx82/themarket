import logging

import pandas as pd
import numpy as np

from articles import Articles

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
        self.transition = {'timestamp': [], 'location': [], 'customer_no': [], 'article': []}

        self.prd = Articles()

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

    def add_to_cart(self, article = None, buy = 0, steal = 0):
        """
        This methods adds the article into the transition and adds the price 
        of it either into the buy oder steal cart.

        Parameters:
            article: name of the article
            buy: price for the shopping cart
            steal: price for the stolen articles
        """
        self.transition['article'].append(article)
        self.stolen_article.append(steal)
        self.shopping_cart.append(buy)

        
    def pick_article(self):
        """
        Picks a random article
        """
        for location in self.transition['location']:
            if location != 'checkout':
                department_articles = self.prd.all_articles[location]
                article_choice = np.random.choice(department_articles)
                article = list(article_choice.keys())[0]
                price = list(article_choice.values())[0]
                self.buy_or_steal(article, price)
            else:
                self.add_to_cart()

    def buy_or_steal(self, article, price):
        """
        Buy or steal article and add them to the corresponding list
        """
        if np.random.uniform() > 0.9:
            logging.info(f"The customer stole {article}.")
            self.add_to_cart(article, steal=price)
        else: 
            self.add_to_cart(article, buy=price)
