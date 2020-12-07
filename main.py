from datetime import datetime

from py_pdf_parser.loaders import load_file

from py_pdf_parser import tables

from zyklus import Zyklus


def load():

    raw_text = ""
    document = load_file("./Data.pdf")
    for el in document.elements:
        raw_text = raw_text + el.text()

    entrys = raw_text.split("Zyklus")
    entrys = entrys[1 : len(entrys)]
    zyklen = []
    for i in range(0, len(entrys), 4):
        zyklen.append(Zyklus(entrys[i : i + 4]))

    for zyklus_el in zyklen:
        zyklus_el.print_csv()


if __name__ == "__main__":
    load()
