from typing import List

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

from pathlib import Path


def parse_obj(lt_objs) -> List[tuple]:
    result = []
    # loop over the object list
    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            text = obj.get_text().replace("\n", "_")
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


def loadvalue_page_date(pdf_path: Path, page: int, date: str) -> str:
    with open(pdf_path, "rb") as file:
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(file)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        result = parse_doc(document, page)
        for el in result:
            print(result)
