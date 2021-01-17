import re
from typing import List

from numpy import ndarray
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

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


def parse_obj(lt_objs) -> List[tuple]:
    result = []
    # loop over the object list
    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            text = obj.get_text().strip("\n").strip(" ")
            text = text.replace("\n", "")

            text = text.replace("DATUM ", "")
            result.append((obj.bbox[0], obj.bbox[1], text))
            # print("%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], text))

            # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            result.extend(parse_obj(obj._objs))

    return result


def parse_doc(doc: PDFDocument, page_nbr: int) -> List[tuple]:
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    doc_result = []

    # loop over all pages in the document
    pages = [el for el in PDFPage.create_pages(doc)]

    desired_page = pages[page_nbr]

    interpreter.process_page(desired_page)
    layout = device.get_result()

    # extract text from this object
    doc_result.extend(parse_obj(layout._objs))

    return doc_result


def extract_dates(koordinate_list: List[tuple]) -> List[tuple]:

    regex = re.compile("[0-9]{2}\.[0-9]{2}\.")

    return [el for el in koordinate_list if re.fullmatch(regex, el[2])]


def load_triples_from_page(pdf_path: Path, page: int) -> List[tuple]:
    with open(pdf_path, "rb") as file:
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(file)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        result = parse_doc(document, page)

        return result
