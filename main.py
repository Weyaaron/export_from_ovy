from pathlib import Path

from src.pdfminer.mine import load_pdf



from src.zyklus import Zyklus


def load():

    list_triple_lists = load_pdf(Path("./data/data.pdf"))

    zyklen = []
    for i in range(len(list_triple_lists)):
        zyklen.append(Zyklus(list_triple_lists[i]))

    for i,zyklus_el in enumerate(zyklen):
       # zyklus_el.extract_bleeding_values(i)
     #   zyklus_el.extract_mukus_values(i)
        print(i)
        print(zyklus_el.dataframe.to_csv())
       # zyklus_el.print_csv()


if __name__ == "__main__":
    #convert_to_image()
    load()
