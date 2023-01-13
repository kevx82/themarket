import os
import logging

import pandas as pd

from tm_generator import TMGenerator
from supermarket import Supermarket

# sets level for logging
logging.basicConfig(level=logging.INFO)

path = 'data/'
day = 'friday'


def run_super_market(super_market):
    super_market.open_market()
    super_market.close_market()
    super_market.pick_articles()
    super_market.calculate_sales()

    return super_market


if __name__ == '__main__':
    logging.info("="*60)
    logging.info("Welcome to the one and only Supermarket")
    logging.info("="*60 + "\n")

    logging.info("Generating Transition Matrix and Entry Vector")

    # initiate the TMGenerator
    tmgen = TMGenerator(path=path)

    # print transition matrix for monday
    logging.info(f"Transition Matrix for {day}: \n {tmgen.tm_dict[day]}\n")
    logging.info(f"Entry Vector: \n {tmgen.entry_dict[day]} \n")

    # initiate the Supermarket
    super_market = Supermarket(tm=tmgen.tm_dict[day], entry=tmgen.entry_dict[day], date="2022-01-02")
    #super_market = 
    run_super_market(super_market)
    
    logging.info(f"\n\nStats for {day} !! \n")
    logging.info(f"Revenue: {round(super_market.revenue, 2)}€")
    logging.info(f"Loss: {round(super_market.loss, 2)}€")
    logging.info(f"Profit: {round(super_market.profit, 2)}€\n")
    
    logging.info(f"Total number of customers: {super_market.customer_no}")
    logging.info(f"Total amount of sold articles: {super_market.sold_articles}")
    logging.info(f"Total amount of stolen articles: {super_market.stolen_articles}")
    

    #day_df = pd.concat([pd.DataFrame(cust.transition) for cust in super_market.customers_inactive], ignore_index=True)
    #print(day_df.groupby(['location'])[['customer_no']].nunique())
    #print(day_df[day_df['customer_no'].isin(range(5))].sort_values(by='timestamp'))
