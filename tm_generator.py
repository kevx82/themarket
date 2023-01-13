import os
import glob
import logging

import pandas as pd


class TMGenerator:

    def __init__(self, path) -> None:
        self.path = path
        self.tm_dict = {}
        self.entry_dict = {}

        # read csv files and save into a dataframe
        self.df = self.read_days()

        # generate the transition matrix based on the dataframe
        self.create_tm()

    def get_weekdays(self):
        return self.df['day'].unique()

    
    def read_days(self):
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

    def get_no_checkout_ids(self, df):
        all_customers = set(df['customer_no'])
        checkout_customers = set(df.loc[df['location'] == 'checkout', 'customer_no'])

        return all_customers.difference(checkout_customers)

    def get_checkout_timestamp(self, df, checkout_time=None):
        if not checkout_time:
            checkout_time = '21:59:59'

        date = df.index.strftime("%Y-%m-%d").unique()[0]

        return date + ' ' + checkout_time

    def get_day_checkouts(self, df, day, no_checkout_id):
        checkouts = []
        datetime = self.get_checkout_timestamp(df)

        for customer in no_checkout_id:
            checkout_df = pd.DataFrame([[customer, 'checkout', day]], columns=df.columns, index=[pd.to_datetime(datetime)])
            checkouts.append(checkout_df)

        return pd.concat(checkouts)


    def append_checkouts(self, df, day):
        no_checkout_id = self.get_no_checkout_ids(df)
        #print(f"Missing checkouts for on {day}: {len(no_checkout_id)}")
        if len(no_checkout_id) > 0:
            checkout_df = self.get_day_checkouts(df, day, no_checkout_id)
            df = pd.concat([df, checkout_df]).sort_values(by=['day', 'customer_no'])
        else:
            print(f"No checkouts missing for: {day}")
        
        # adding index name as it gets lost while appending the checkouts
        df.index.name = 'timestamp'

        return df

    def resample_df(self, df):
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



            