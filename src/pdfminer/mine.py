import re
from typing import List

import minecart


from pathlib import Path



def filter_dates(koordinate_list: List[tuple]) -> List[tuple]:

    date_reg = re.compile("[0-9]{2}\.")
    date_list = [el for el in koordinate_list if re.fullmatch(date_reg, el[2])]

    result = []

    for i in range(0, len(date_list) - 1,2):
        final_date = date_list[i][2] + date_list[i+1][2]
        result.append((date_list[i][0], date_list[i][1],final_date))

    return result


def load_text(pdf_path:Path)->str:
    result = ""
    with open(pdf_path, "rb") as file:
        doc = minecart.Document(file)
        for i in range(0, 24):
            page = doc.get_page(i)

            for letter_el in page.letterings:
                result +=  str(letter_el)
    return result



def load_triples_from_page(pdf_path:Path, page_nmbr:int)->List[tuple]:
    result = []
    with open(pdf_path, "rb") as file:

        doc = minecart.Document(file)
        page = doc.get_page(page_nmbr)

        for letter_el in page.letterings:
            text = str(letter_el).strip("\n").strip(" ")
            text = text.replace("\n", "")
            text = text.replace("DATUM ", "")

            bbox = letter_el.get_bbox()
            result.append((int(bbox[0]), int(bbox[1]), str(text)))

    return result





def extract_shapes_from_page(pdf_path:Path, page_nmbr:int)->List:
    target_color = (1, 0, 0.498039)
    with  open(pdf_path, 'rb') as file:
        doc = minecart.Document(file)
        page = doc.get_page(page_nmbr)

        filled_shapes = [el for el in page.shapes if el.fill is not None]
        stroked_shapes = [el for el in page.shapes if el.stroke is not None]

        filled_shapes = [el for el in filled_shapes if el.fill.color.as_rgb() == target_color]
        stroked_shapes = [el for el in stroked_shapes if el.stroke.color.as_rgb() == target_color]

    return filled_shapes
