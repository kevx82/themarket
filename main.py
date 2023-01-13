import os
import logging

import pandas as pd

from tm_generator import TMGenerator
from supermarket import Supermarket

# sets level for logging
logging.basicConfig(level=logging.INFO)

path = 'data/'
day = 'friday'


if __name__ == '__main__':

    print("starting generator")

    # initiate the TMGenerator
    tmgen = TMGenerator(path=path)

    # initiate the Supermarket
    super_market = Supermarket(tm=tmgen.tm_dict[day], entry=tmgen.entry_dict[day], date="2022-01-02")

    # print transition matrix for monday
    logging.info(tmgen.tm_dict[day])
    logging.info(tmgen.entry_dict[day])
    super_market.open_market()
    super_market.close_market()
    day_df = pd.concat([pd.DataFrame(cust.transition) for cust in super_market.customers_inactive], ignore_index=True)
    print(day_df[day_df['customer_no'] == 1])
    print([cust.transition for cust in super_market.customers_inactive[:5]])

