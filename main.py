from pathlib import Path

from src.pdfminer.mine import load_pdf

from src.zyklus import Zyklus


def load():

    list_triple_lists = load_pdf(Path("./data/data.pdf"))
    zyklen = []
    for i in range(len(list_triple_lists)):
        new_zyklus = Zyklus(list_triple_lists[i])
        print(new_zyklus.print_csv())

if __name__ == "__main__":
    load()
