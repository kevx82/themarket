import os
import glob

import pandas as pd


class TMGenerator:

    def __init__(self, path) -> None:
        """
        This method initiates the TMGenerator
        
        Args:
            path: path to the file to generate the transition matrix
        """
        self.path = path
        self.tm_dict = {}
        self.entry_dict = {}

        # read csv files and save into a dataframe
        self.df = self.read_days()

        # generate the transition matrix based on the dataframe
        self.create_tm()

    def get_weekdays(self) -> list:
        """
        This method returns a list with weekdays
        
        Returns:
            list of weekdays
        """
        return list(self.df['day'].unique())
    
    def read_days(self) -> pd.DataFrame:
        """
        This methods reads all csv fle from the path and returns oned ataframe for days.

        Returns: 
            dataframe
        """
        days = []

        # creates search string in a path
        path = os.path.join(self.path, "*.csv")

        for file in glob.glob(path):
            df = pd.read_csv(file, sep=';', parse_dates=[0], index_col=[0])
            # getting the file name
            day = file.split('/')[-1].split('.')[0]
            df['day'] = day
            days.append(df)

        return  pd.concat(days)

    def get_no_checkout_ids(self, df) -> set:
        """
        This method returns all numbers of customers for a day that didn't checkout.
        
        Args:
            df: dataframe containing customer ids

        Returns:
            set of numbers
        """
        # creates a set of all customer numbers
        all_customers = set(df['customer_no'])

        # creates a set of all customers with checkout
        checkout_customers = set(df.loc[df['location'] == 'checkout', 'customer_no'])

        return all_customers.difference(checkout_customers)

    def get_checkout_timestamp(self, df, checkout_time=None) -> str:
        """
        This method generates a timestamp for the checkout of the current day as string.
        
        Args:
            df: dataframe containing datetimes
            checkout_time: time for checkout

        Returns: 
            string with timestamp
        """
        # if no specific checkout time is set the following wil be used
        if not checkout_time:
            checkout_time = '21:59:00'

        # converts datetime into string and takesthe first value of the unqiue list
        date = df.index.strftime("%Y-%m-%d").unique()[0]

        return date + ' ' + checkout_time

    def append_checkouts(self, df, day):
        """
        This methods appends the missing checkouts for each customer.
        
        Args:
            df: dataframe with transitions for each customer
            day: name of the weekday

        Returns:
            df: dataframe with added checkouts
        """
        no_checkout_id = self.get_no_checkout_ids(df)

        if len(no_checkout_id) > 0:
            datetime = self.get_checkout_timestamp(df)
            for customer in no_checkout_id:
                checkout_df = pd.DataFrame([[customer, 'checkout', day]], columns=df.columns, index=[pd.to_datetime(datetime)])
                pd.concat([df, checkout_df])

        df.index.name = 'timestamp'
        df = df.sort_values(by= 'customer_no')

        return df

    def resample_df(self, df):
        """
        This method resample the timestamp to 1 minute steps.

        Returns:
            df: dataframe with resampled timestamps
        """
        df = df.groupby(['customer_no']).resample('1min').last().ffill()
        df = df.drop(columns=['customer_no', 'day'])
        df = df.reset_index().set_index('timestamp')
        
        return df

    def create_tm(self):
        """
        This methods creates for all days a transition matrix and an entry vector and 
        saves them in a dict for each day.
        """
        weekdays = self.get_weekdays()        

        for day in weekdays: 
            # creates subset of dataframe for current day
            day_df = self.df[self.df['day'] == day].copy()

            # appends missing checkouts
            day_df = self.append_checkouts(day_df, day)

            # resample timestamp to 1 min steps
            day_df = self.resample_df(day_df)

            # adds column from with previos location
            day_df['from'] = day_df['location'].shift(1).fillna('checkout')

            # creates transition matrix
            tm_df = pd.crosstab(day_df['from'], day_df['location'], normalize='index')

            # save entry probabilities in entry dict
            self.entry_dict[day] = list(tm_df[tm_df.index == 'checkout'].values[0])

            # creates correct transition for checkout
            checkout = pd.DataFrame([[1, 0 , 0 , 0, 0]], index=['checkout'], columns=tm_df.columns)

            # drops entry probabilities
            tm_df = tm_df.drop('checkout')

            # concat checkout column
            tm_df = pd.concat([tm_df, checkout])

            # save transition matrix in dict
            self.tm_dict[day] = tm_df



            