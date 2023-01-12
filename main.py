import os

import pandas as pd

from tm_generator import TMGenerator


path = '../data/'


if __name__ == '__main__':

    print("starting generator")

    # initiate the TMGenerator
    tmgen = TMGenerator(path=path)

    # print transition matrix for monday
    print(tmgen.tm_dict['monday'])

