import re
from typing import List

import minecart
from numpy import ndarray



from pathlib import Path

from src.imageprocessing.utils import tuple_diff


def color_gradient_from_xy(image, x_offset, y_offset) -> int:
    result = 0
    height = 30
    width = 30

    middle_tuple = image[x_offset + height / 2, y_offset + width / 2]
    for x in range(x_offset, x_offset + height):
        for y in range(y_offset, y_offset + width):
            diff = tuple_diff(middle_tuple, image[x, y])
            result += diff
            if (
                x == x_offset
                or y == x_offset
                or x == x_offset + height - 1
                or y == y_offset + width - 1
            ):
                image[x, y] = (100, 100, 100)

    return result

    pass


def color_gradient(image_matrix: ndarray) -> int:
    sum_result = 0
    x_center = int(image_matrix.shape[0] / 2)
    y_center = int(image_matrix.shape[1] / 2)
    midle_tuple = image_matrix[x_center, y_center]

    for x in range(0, image_matrix.shape[0]):
        for y in range(0, image_matrix.shape[1]):
            target_tuple = image_matrix[x, y]
            result = tuple_diff(midle_tuple, target_tuple)
            sum_result += result

    return sum_result



def extract_dates(koordinate_list: List[tuple]) -> List[tuple]:

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





