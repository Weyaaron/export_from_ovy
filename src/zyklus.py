from datetime import datetime

from src.pdfminer.mine import load_triples_from_page, filter_dates, extract_shapes_from_page, filter_temps
import pandas as pd

from src.pdfminer.pdfpagecontainer import PdfPageContainer
from src.utils import load_frame



class Zyklus:
    def __init__(self, pdf_page: PdfPageContainer) -> None:

        self.dataframe = load_frame()

        self.pdf_page = pdf_page
        self.length = 0
        self.date_range = ""
        self.year = 0
        self.date_list = []
        self.temp_list = []
        self.time_list = []



    def print_csv(self):
        lines = ""

        for i, date_el in enumerate(self.date_list):
            new_line = ""
            date_result = datetime.strptime(date_el, "%d.%m.%Y")
            final_str = date_result.strftime("%Y-%m-%d")
            new_line = new_line + final_str + ","
            try:
                new_line = new_line + self.temp_list[i] + ",false,"
                new_line = new_line + self.time_list[i]
            except IndexError:
                new_line = new_line + "NONE,false,"
                new_line = new_line + "NONE"
            lines = lines + new_line + "\n"
        print(lines)

    def extract_length(self):
        self.length = int(self.pdf_page[2].split(": ")[1])

    def extract_date_range(self):
        critical_part = self.pdf_page[3].split("D")[0]
        self.date_range = critical_part.split(": ")[1].split(" ")[0]

        self.year = int( str(self.date_range.split(".")[2]))

    def extract_temps(self):
        str_val = self.pdf_page[3].split("Exportiert")[0]
        temps = str_val.split("BT")[1].split("PERIO")[0]

        counties_temps = temps.replace("\n", "")
        for i in range(0, len(counties_temps), 5):
            single_temp = counties_temps[i : i + 5]
            single_temp = single_temp.replace(",", ".")
            self.temp_list.append(single_temp)

        triples = load_triples_from_page('./data/data.pdf', self.page)
        temp_triples = filter_temps(triples)

        result = []
        for shape_el in shapes:
            x_koordinate = shape_el.path[0][1]
            min_distance = 10
            date_found = None
            for tuple_el in date_triples:
                distance = int(abs(tuple_el[0] - x_koordinate))
                if distance < min_distance:
                    min_distance = distance
                    date_found = tuple_el
            result.append((shape_el, date_found))

        for i in range(0, len(self.dataframe.index)):
         #   self.dataframe = self.dataframe.at[i, 'temperature.value'] = "Hallo"
           self.dataframe.loc[self.dataframe.index == i, 'temperature.value'] = self.temp_list[i]
           self.dataframe.loc[self.dataframe.index == i, 'temperature.exclude'] = "None"


    def extract_dates(self):
        date_str = self.pdf_page[3].split("DATUM")[1]
        date_pieces = date_str.split("UHR")[0].split(".")
        for i in range(0, len(date_pieces)-1,2):
            current_piece = date_pieces[i]
            next_piece = date_pieces[i+1]
            new_value = ".".join([current_piece, next_piece, str(self.year)])
            self.date_list.append(new_value)

        for date_el in self.date_list:
            date_result = datetime.strptime(date_el, "%d.%m.%Y")
            new_series = pd.Series({"date":date_result})
            self.dataframe = self.dataframe.append(new_series, ignore_index=True)


            final_str = date_result.strftime("%Y-%m-%d")

    def extract_times(self):
        time_str = self.pdf_page[3].split("UHRZEIT")[1].split("37,00")[0]
        continuous_time = time_str.replace("\n", "")
        for i in range(0, len(continuous_time), 5):
            self.time_list.append(continuous_time[i : i + 5])

        for i in range(0, len(self.dataframe.index)):
            #   self.dataframe = self.dataframe.at[i, 'temperature.value'] = "Hallo"
            self.dataframe.loc[self.dataframe.index == i, 'temperature.time'] = self.time_list[i]


    def extract_bleeding_values(self, page_nmbr:int)->None:
        shapes = extract_shapes_from_page('./data/data.pdf',page_nmbr)
        triples = load_triples_from_page('./data/data.pdf', page_nmbr)
        date_triples = filter_dates(triples)

        result = []
        for shape_el in shapes:
            x_koordinate = shape_el.path[0][1]
            min_distance = 10
            date_found = None
            for tuple_el in date_triples:
                distance = int(abs(tuple_el[0]-x_koordinate))
                if distance<min_distance:
                    min_distance = distance
                    date_found = tuple_el
            result.append((shape_el, date_found))


    def extract_mukus_values(self, page_nmbr: int)->None:

        triples = load_triples_from_page('./data/data.pdf',page_nmbr)
        date_triples  = filter_dates(triples)

        tuples_found = []

        allowed_values = ["S","t","S+"]
        str_values_present = [el for el in triples if el[2] in allowed_values ]

        for tuple_a in date_triples:
            min_distance = 10
            matching_tuple = None

            for tuple_b in str_values_present:
                distance =  abs(tuple_a[0]- tuple_b[0])
                if distance < min_distance:
                    min_distance = distance
                    matching_tuple = tuple_b
            if matching_tuple:
                tuples_found.append((tuple_a,matching_tuple, min_distance))

        if len(str_values_present) != len(tuples_found):
            raise ValueError