import logging

import pandas as pd
import numpy as np

from customer import Customer


class Supermarket:

    def __init__(self, tm: pd.DataFrame, date:str, open:str = "7:00", close:str = "22:00") -> None:
        """
        This method initiates the Supermarket class.

        Attributes:
            tm: dataframe containing the transition matrix for current day
            date: date of the current day
            open: time the supermarket opens (default 7:00)
            close: time the supermarket opens (default 7:00)
        """

        self.tm = tm
        self.date = date
        self.open = self.create_datetime(self.date, open)
        self.close = self.create_datetime(self.date, close)

        # current datetime of the day
        self.timestamp = None

        # count of total customers entered the market
        self.customer_id = 0

        # revenue of the current day
        self.revenue = None

        # list of customers in the supermarket
        self.customer_active = []

        # list of customers that checked out
        self.customer_inactive = []

    def create_datetime(self, date, time):
        """
        In this method a datetime will be created based on the passed date and time

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
        if np.random.uniform() > 0.3:
            customer = Customer(self.tm, self.entry)
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
        # checking in the transition dict of each customer if the last location is checkout and adds them to checkout list of supermarket
        self.customers_inactive.extend([customer for customer in self.customers_active if customer.transition['location'][-1] == 'checkout'])
        # updating the list of all customers in the supermarket whose last location is not checkout
        self.customers_active[:] = [customer for customer in self.customers_active if customer.transition['location'][-1] != 'checkout']

    def open_market(self):
        """
        In this method new customers enter the supermarket, move around and checkout at the end.
        """
        current_time =  self.open
        self.update_timestamp(current_time)
        while current_time < self.close:
            self.move_customer()
            self.add_customer()
            self.checkout_customer()
            if self.current_time.minute == 0:
                logging.info(f"current time: {self.current_time}")
            current_time = self.current_time + pd.DateOffset(minutes=1)
            self.update_timestamp(current_time)

    def close_market(self):
        """
        In this method the supermarket closes. The location of all customers in the supermarket  
        is set to checkout and their transition updated with the new timestamp and location. 
        Afterwards all customer will be moved to the check out list.
        """
        for customer in self.customers_active:
            customer.location = 'checkout'
            customer.add_transition(self.timestamp)
    
        self.checkout_customer()

    def calculate_revenue(self):
        pass

    def pick_products(self):
        pass
