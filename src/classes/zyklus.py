from datetime import datetime

from src.mine import filter_dates, filter_temps, filter_times
import pandas as pd

from src.classes.pdfpagecontainer import PdfPageContainer
from src.utils import load_frame, bind_dates_with_data


class Zyklus:
    def __init__(self, pdf_page: PdfPageContainer) -> None:

        self.dataframe = load_frame()
        self.pdf_page = pdf_page
        self.length = 0
        self.year = 0


    def extract_temps(self):

        date_triples = filter_dates(self.pdf_page.triples)
        temp_triples = filter_temps(self.pdf_page.triples)

        bound_temps = bind_dates_with_data(date_triples, temp_triples)

        def map_temp(key_el):
            match_str = key_el.strftime("%d.%m") + "."
            value= bound_temps[match_str]
            if value is None:
                return 'None'
            return value

        def map_false(arg):
            return False

        self.dataframe["temperature.value"] = self.dataframe["date"].map(map_temp)
        self.dataframe["temperature.exclude"] = self.dataframe["date"].map(map_false)
        self.dataframe.drop(
            index=self.dataframe[self.dataframe["temperature.value"] == "None"].index,
            inplace=True,
        )

    def extract_dates(self):
        date_triples = filter_dates(self.pdf_page.triples)

        year = self.pdf_page.triples[3][2].split(".")[4]
        for triple_el in date_triples:
            date_str = triple_el[2] + year
            date_result = datetime.strptime(date_str, "%d.%m.%Y")
            new_series = pd.Series({"date": date_result})
            self.dataframe = self.dataframe.append(new_series, ignore_index=True)


    def extract_times(self):
        time_tuples = filter_times(self.pdf_page.triples)
        date_tuples = filter_dates(self.pdf_page.triples)

        bound_data = bind_dates_with_data(date_tuples, time_tuples)

        def map_dict(key_el):

            match_str = key_el.strftime("%d.%m") + "."
            try:
                return bound_data[match_str]
            except KeyError:
                return None

        self.dataframe["temperature.time"] = self.dataframe["date"].map(map_dict)

    def extract_bleeding_values(self) -> None:
        shapes = self.pdf_page.shapes
        triples = self.pdf_page.triples
        date_triples = filter_dates(triples)

        result = {}
        for shape_el in shapes:
            x_koordinate = shape_el.path[0][1]
            min_distance = 10
            date_found = None
            for tuple_el in date_triples:
                distance = int(abs(tuple_el[0] - x_koordinate))
                if distance < min_distance:
                    min_distance = distance
                    date_found = tuple_el
            result.update({date_found[2]: shape_el})

        def map_bleeding(date_arg):
            length_type = {13: 2, 7: 3, 14: 1}

            match_str = date_arg.strftime("%d.%m") + "."
            try:
                shape = result[match_str]
            except KeyError:
                return None
            return length_type[len(shape.path)]

        self.dataframe["bleeding.value"] = self.dataframe["date"].map(map_bleeding)

        def map_false(arg):
            return False

        self.dataframe["bleeding.exclude"] = self.dataframe["date"].map(map_false)

    def extract_mukus_values(
        self,
    ):
        triples = self.pdf_page.triples
        date_triples = filter_dates(triples)

        allowed_values = ["S", "S+"]
        str_values_present = [el for el in triples if el[2] in allowed_values]

        bound_values = bind_dates_with_data(date_triples, str_values_present)

        def map_feeling(arg):
            match_str = arg.strftime("%d.%m") + "."
            if match_str in bound_values.keys():
                return 1
            return 0

        def map_texture(arg):
            match_str = arg.strftime("%d.%m") + "."

            try:
                value = bound_values[match_str]
                #todo: Explore the none value
            except KeyError:
                return None

            if value == "S+":
                return 2
            if value == "S":
                return 1
            return 0

        def map_false(arg):
            return False

        self.dataframe["mucus.feeling"] = self.dataframe["date"].map(map_feeling)
        self.dataframe["mucus.texture"] = self.dataframe["date"].map(map_texture)
        self.dataframe["mucus.exclude"] = self.dataframe["date"].map(map_false)
        self.dataframe["mucus.value"]  = self.dataframe["mucus.feeling"] + self.dataframe["mucus.texture"]


