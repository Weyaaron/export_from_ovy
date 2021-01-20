

import pandas as pd











def load_frame()->pd.DataFrame():

    frame= pd.read_csv('./template.csv')
    return frame