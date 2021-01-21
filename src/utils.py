from typing import List
import pandas as pd


def bind_dates_with_data(date_triples, data_triples) -> dict:
    result = {}
    for tuple_date_el in date_triples:
        min_distance = 10
        data_found = "None"

        for tuple_data_el in data_triples:
            distance = int(abs(tuple_data_el[0] - tuple_date_el[0]))
            if distance < min_distance:
                min_distance = distance
                data_found = tuple_data_el[2]
            result.update({tuple_date_el[2]: data_found})

    return result


def load_frame() -> pd.DataFrame():

    frame = pd.read_csv("./template.csv")

    return frame
