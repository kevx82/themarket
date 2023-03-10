import logging

import pandas as pd
import numpy as np

from customer import Customer


class Supermarket:

    def __init__(self, tm: pd.DataFrame, entry: list, date:str, open:str = "7:00", close:str = "22:00") -> None:
        """
        This method initiates the Supermarket class.

        Attributes:
            tm: dataframe containing the transition matrix for current day
            entry: list of probabilities for the first location of a customer
            date: date of the current day
            open: time the supermarket opens (default 7:00)
            close: time the supermarket opens (default 7:00)
        """

        self.tm = tm
        self.entry = entry
        self.date = date
        self.open = self.create_datetime(self.date, open)
        self.close = self.create_datetime(self.date, close)

        # current datetime of the day
        self.timestamp = None

        # count of total customers entered the market
        self.customer_no = 0

        # revenue of the current day
        self.revenue = 0
        self.loss = 0
        self.profit = 0

        # article information
        self.sold_articles = 0
        self.stolen_articles = 0

        # list of customers in the supermarket
        self.customers_active = []

        # list of customers that checked out
        self.customers_inactive = []

    def create_datetime(self, date, time) -> pd.DatetimeIndex:
        """
        In this method a datetime will be created based on the passed date and time
        
        Args:
            date: date of the current day
            time: time of the current day

        Returns:
            datetime: timestamp of date and time
        """
        return pd.to_datetime(date + ' ' + time)

    def update_timestamp(self, timestamp):
        """
        This methods turns the datetime object into a string and saves it in the timestamp.

        Parameters:
            timestamp: datetime object of current time in the supermarket
        """
        self.timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def add_customer(self):
        """
        This method add new customers to the supermarket. The chance to add a new customer is 70%.
        """
        if np.random.uniform() > 0.2:
            self.customer_no += 1
            customer = Customer(self.tm, self.entry, self.customer_no)
            customer.add_transition(self.timestamp)
            self.customers_active.append(customer)

    def move_customer(self):
        """
        This method loops through all customers in the supermarket and moves each of them.
        """
        for customer in self.customers_active:
            customer.move(self.timestamp)

    def checkout_customer(self):
        """
        This method loops through all customers in the supermarket. All customers located in the checkout 
        will be added to the checkout list. Afterwards the list of customers not located in the checkout will
        be updated.
        """
        # checking in the transition dict of each customer if the last location is checkout
        checkout = [customer for customer in self.customers_active if customer.transition['location'][-1] == 'checkout']
        # adds checked out customer to checkout list of supermarket
        self.customers_inactive.extend(checkout)

        # updating the list of all customers in the supermarket whose last location is not checkout
        self.customers_active[:] = [customer for customer in self.customers_active if customer.transition['location'][-1] != 'checkout']

    def open_market(self):
        """
        In this method new customers enter the supermarket, move around and checkout at the end.
        """
        # declare current time as opening time
        current_time =  self.open
        # set global time of supermarket to timestamp
        self.update_timestamp(current_time)

        # loop (supermarket open) until closing time and simulate customers
        while current_time < self.close:
            self.move_customer()
            self.add_customer()
            self.checkout_customer()
            if current_time.minute == 0:
                logging.info(f"current time: {current_time}")
            # increase current time by 1 minute
            current_time = current_time + pd.DateOffset(minutes=1)
            # update global time of supermarket to timestamp
            self.update_timestamp(current_time)

    def close_market(self):
        """
        In this method the supermarket closes. The location of all customers in the supermarket  
        is set to checkout and their transition updated with the new timestamp and location. 
        Afterwards all customer will be moved to the check out list.
        """
        # loop through all active customers
        for customer in self.customers_active:
            # set location of customer to checkout
            customer.location = 'checkout'
            # adds the new location and timestamp to the transitions
            customer.add_transition(self.timestamp)
    
        self.checkout_customer()

    def calculate_sales(self):
        """
        This method calculates the revenue, loss, profit, sold and stolen articles for all customers.
        """
        for customer in self.customers_inactive:
            sold = len([price for price in customer.shopping_cart if price > 0])
            stolen = len([price for price in customer.stolen_article if price > 0])
            
            # calculates values for sold articles in shopping cart
            self.revenue = self.revenue + sum(customer.shopping_cart)
            self.sold_articles = self.sold_articles + sold

            # calculates values for stolen articles in stolen articles
            self.loss = self.loss + sum(customer.stolen_article)
            self.stolen_articles = self.stolen_articles + stolen

            # calculates total profit based on sold and stolen articles
            self.profit = self.revenue - self.loss


    def pick_articles(self):
        """
        In this method each customer will pick articles for each transition. All prices for bought and stolen
        products will be added to the transition.
        """
        for customer in self.customers_inactive:
            customer.pick_article()
            customer.transition['bought'] = customer.shopping_cart
            customer.transition['stolen'] = customer.stolen_article
