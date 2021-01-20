from pathlib import Path

from src.pdfminer.mine import load_text



from src.zyklus import Zyklus


def load():

    raw_text = ""
    entrys = load_text(Path("./data/data.pdf")).split("Zyklus")

    entrys = entrys[1 : len(entrys)]
    #for speed purposes
   # entrys = entrys[0:4]
    zyklen = []
    for i in range(0, len(entrys), 4):
        zyklen.append(Zyklus(entrys[i : i + 4]))

    for i,zyklus_el in enumerate(zyklen):
        zyklus_el.extract_bleeding_values(i)
        zyklus_el.extract_mukus_values(i)
        print(i)
       # zyklus_el.print_csv()


if __name__ == "__main__":
    #convert_to_image()
    load()
