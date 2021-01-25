import re
from typing import List

import minecart

from pathlib import Path

from src.classes.pdfpagecontainer import PdfPageContainer


def filter_dates(koordinate_list: List[tuple]) -> List[tuple]:

    date_reg = re.compile("[0-9]{2}\.")
    date_list = [el for el in koordinate_list if re.fullmatch(date_reg, el[2])]

    result = []

    for i in range(0, len(date_list) - 1, 2):
        final_date = date_list[i][2] + date_list[i + 1][2]
        result.append((date_list[i][0], date_list[i][1], final_date))

    return result


def filter_times(triples) -> List:
    past_index = False
    temp_list = []

    for tuple_el in triples:
        # rather hacky, might break
        if "," in tuple_el[2]:
            past_index = False
        if past_index:
            temp_list.append(tuple_el)
        if tuple_el[2] == "UHRZEIT":
            past_index = True

    result = []
    for i in range(0, len(temp_list) - 1, 2):
        final_temp = temp_list[i][2] + temp_list[i + 1][2]
        result.append((temp_list[i][0], temp_list[i][1], final_temp))

    return result


def filter_temps(triples) -> List:

    past_index = False
    temp_list = []

    for tuple_el in triples:
        if tuple_el[2] == "PERIODE":
            past_index = False
        if past_index:
            temp_list.append(tuple_el)
        if tuple_el[2] == "BT":
            past_index = True

    result = []
    for i in range(0, len(temp_list) - 1, 2):
        final_temp = temp_list[i][2] + temp_list[i + 1][2]
        final_temp = final_temp.replace(",", ".")
        result.append((temp_list[i][0], temp_list[i][1], final_temp.strip('"')))

    return result


def load_pdf(pdf_path: Path) -> List[PdfPageContainer]:

    target_color = (1, 0, 0.498039)
    list_result = []
    with open(pdf_path, "rb") as file:

        doc = minecart.Document(file)

        for page_el in doc.iter_pages():
            new_container = PdfPageContainer()
            for letter_el in page_el.letterings:
                bbox = letter_el.get_bbox()
                new_container.triples.append(
                    (int(bbox[0]), int(bbox[1]), str(letter_el))
                )

            filled_shapes = [el for el in page_el.shapes if el.fill is not None]
            new_container.shapes = [
                el for el in filled_shapes if el.fill.color.as_rgb() == target_color
            ]

            list_result.append(new_container)
    return list_result
