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

    def create_tm(self):
        """
        This methods creates for all days a transition matrix and an entry vector and 
        saves them in a dict for each day.
        """
        weekdays = self.get_weekdays()        

        for day in weekdays:
            # creates subset of dataframe for current day
            day_df = self.df[self.df['day'] == day].copy()

            # adds column from with previos location
            day_df['from'] = day_df['location'].shift(1).fillna('checkout')

            # creates transition matrix
            tm_df = pd.crosstab(day_df['from'], day_df['location'], normalize='index')

            # save entry probabilities in entry dict
            self.entry_dict[day] = tm_df[tm_df.index == 'checkout'].values

            # creates correct transition for checkout
            checkout = pd.DataFrame([[1, 0 , 0 , 0, 0]], index=['checkout'], columns=tm_df.columns)

            # drops entry probabilities
            tm_df = tm_df.drop('checkout')

            # concat checkout column
            tm_df = pd.concat([tm_df, checkout])

            # save transition matrix in dict
            self.tm_dict[day] = tm_df



            