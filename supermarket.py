import logging

import pandas as pd


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
        self.current_time = None
        # revenue of the current day
        self.revenue = None
        self.customer_active = []
        self.customer_inactive = []

    def create_datetime(self, date, time):
        """
        In this method a datetime will be created based on the passed date and time

        Returns:
            datetime: timestamp of date and time
        """
        return pd.to_datetime(date + ' ' + time)

    def move_customer(self):
        pass

    def check_state(self):
        pass

    def checkout_customer(self):
        pass

    def add_customer(self):
        pass

    def open_market(self):
        self.current_time =  self.open
        while self.current_time < self.close:
            if self.current_time.minute == 0:
                logging.info(f"current time: {self.current_time}")
            self.current_time = self.current_time + pd.DateOffset(minutes=1)

    def close_market():
        pass

    def calculate_revenue(self):
        pass

    def pick_products(self):
        pass
